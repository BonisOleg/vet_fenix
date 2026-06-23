(() => {
  const menu = document.getElementById('mobile-menu');
  const toggleBtn = document.querySelector('[data-menu-toggle]');

  const openMenu = () => {
    if (!menu) {
      return;
    }
    menu.hidden = false;
    menu.classList.add('is-open');
    document.body.classList.add('menu-open');
    toggleBtn?.setAttribute('aria-expanded', 'true');
  };

  const closeMenu = () => {
    if (!menu) {
      return;
    }
    menu.classList.remove('is-open');
    document.body.classList.remove('menu-open');
    toggleBtn?.setAttribute('aria-expanded', 'false');
    window.setTimeout(() => {
      if (!menu.classList.contains('is-open')) {
        menu.hidden = true;
      }
    }, 250);
  };

  toggleBtn?.addEventListener('click', () => {
    if (menu?.classList.contains('is-open')) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  document.querySelectorAll('[data-menu-close]').forEach((el) => {
    el.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu?.classList.contains('is-open')) {
      closeMenu();
      toggleBtn?.focus();
    }
  });
})();
