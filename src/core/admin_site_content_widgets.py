from __future__ import annotations

from typing import Any, Optional

from django.contrib.admin.widgets import AdminTextInputWidget, AdminTextareaWidget
from django.forms import CheckboxInput, ClearableFileInput, FileInput, Select, SelectMultiple
from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES

# Classes that forced always-dark inputs (legacy). Strip them so light theme works.
_STRIP_CLASSES = frozenset(
    {
        'bg-base-900',
        'text-base-100',
        'border-base-700',
    }
)

_THEME_CLASSES = (
    'bg-white',
    'text-font-default-light',
    'border-base-200',
    'placeholder-base-400',
    'dark:bg-base-900',
    'dark:text-font-default-dark',
    'dark:border-base-700',
)

_SKIP_WIDGET_TYPES = (
    CheckboxInput,
    Select,
    SelectMultiple,
    FileInput,
    ClearableFileInput,
)


def cms_control_classes(base_classes: list[str], extra_class: str = '') -> str:
    classes: list[str] = []
    for item in base_classes:
        if item in _STRIP_CLASSES:
            continue
        if item not in classes:
            classes.append(item)
    for token in _THEME_CLASSES:
        if token not in classes:
            classes.append(token)
    if extra_class:
        for token in extra_class.split():
            if token in _STRIP_CLASSES:
                continue
            if token not in classes:
                classes.append(token)
    return ' '.join(classes)


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop('class', '')
        super().__init__(
            attrs={
                **merged,
                'class': cms_control_classes(INPUT_CLASSES, extra_class),
            }
        )


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop('class', '')
        super().__init__(
            attrs={
                **merged,
                'class': cms_control_classes(TEXTAREA_CLASSES, extra_class),
            }
        )


ReadableAdminTextInputWidget = CmsAdminTextInputWidget
ReadableAdminTextareaWidget = CmsAdminTextareaWidget
readable_control_classes = cms_control_classes


def apply_readable_widget(widget):
    try:
        from tinymce.widgets import TinyMCE
    except ImportError:
        TinyMCE = ()  # type: ignore[misc, assignment]

    if isinstance(widget, TinyMCE):
        return widget

    if isinstance(widget, _SKIP_WIDGET_TYPES):
        return widget

    attrs = getattr(widget, 'attrs', None)
    if not attrs:
        return widget

    css = attrs.get('class', '')
    if not any(
        token in css
        for token in ('bg-white', 'bg-base-900', 'text-font-default-light', 'border-base-200')
    ):
        return widget

    merged_attrs = dict(attrs)
    if isinstance(widget, AdminTextareaWidget):
        return CmsAdminTextareaWidget(attrs=merged_attrs)
    return CmsAdminTextInputWidget(attrs=merged_attrs)
