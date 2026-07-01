from django.core.management.base import BaseCommand, CommandError

from core.admin_site_content import load_section_blocks
from core.block_defaults import BLOCK_DEFAULTS, VISIBILITY_SUFFIX
from core.context_processors import SITE_BLOCKS_CACHE_KEY
from core.models import SiteBlock
from core.site_content_registry import get_section


class Command(BaseCommand):
    help = 'Скинути CMS-блоки секції до значень з BLOCK_DEFAULTS'

    def add_arguments(self, parser):
        parser.add_argument('page_slug', help='Напр. home, services, site')
        parser.add_argument('section_slug', help='Напр. hero, header, footer-social')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показати зміни без запису в БД',
        )

    def handle(self, *args, **options):
        page_slug = options['page_slug']
        section_slug = options['section_slug']
        dry_run = options['dry_run']

        try:
            section = get_section(page_slug, section_slug)
        except KeyError as exc:
            raise CommandError(f'Секцію не знайдено: {page_slug}/{section_slug}') from exc

        blocks = load_section_blocks(section)
        updated = 0

        for block in blocks.values():
            default = BLOCK_DEFAULTS.get(
                (block.page, block.key),
                '1' if block.key.endswith(VISIBILITY_SUFFIX) else '',
            )
            if block.content_type == SiteBlock.ContentType.TEXT:
                if block.text_html == default:
                    continue
                self.stdout.write(f'  {block.page}.{block.key}: "{block.text_html[:40]}..." → default')
                if not dry_run:
                    block.text_html = default
                    block.save(update_fields=['text_html'])
                updated += 1
            elif block.content_type == SiteBlock.ContentType.IMAGE and block.image:
                self.stdout.write(f'  {block.page}.{block.key}: image cleared')
                if not dry_run:
                    block.image.delete(save=False)
                    block.image = ''
                    block.save(update_fields=['image'])
                updated += 1

        if not dry_run and updated:
            from django.core.cache import cache

            cache.delete(SITE_BLOCKS_CACHE_KEY)

        label = section.sidebar_title or section.title
        if dry_run:
            self.stdout.write(self.style.WARNING(f'[dry-run] {label}: {updated} блок(ів) буде скинуто'))
            return

        self.stdout.write(self.style.SUCCESS(f'{label}: скинуто {updated} блок(ів)'))
