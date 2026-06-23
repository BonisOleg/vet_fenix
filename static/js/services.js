(() => {
  let openSlug = null;

  document.body.addEventListener('htmx:beforeRequest', (event) => {
    const trigger = event.detail.elt;
    if (!trigger?.hasAttribute('data-service-toggle')) {
      return;
    }
    const targetSel = trigger.getAttribute('hx-target');
    if (!targetSel) {
      return;
    }
    const panel = document.querySelector(targetSel);
    if (!panel) {
      return;
    }
    const slug = panel.id.replace('panel-', '');
    if (openSlug === slug && panel.innerHTML.trim()) {
      event.preventDefault();
      panel.innerHTML = '';
      panel.closest('.svc-row')?.classList.remove('is-open');
      trigger.setAttribute('aria-expanded', 'false');
      openSlug = null;
    }
  });

  document.body.addEventListener('htmx:afterSwap', (event) => {
    const panel = event.detail.target;
    if (!panel.id || !panel.id.startsWith('panel-')) {
      return;
    }
    const slug = panel.id.replace('panel-', '');
    document.querySelectorAll('.svc-row-panel').forEach((other) => {
      if (other === panel) {
        return;
      }
      other.innerHTML = '';
      other.closest('.svc-row')?.classList.remove('is-open');
      const btn = other.closest('.svc-row')?.querySelector('[data-service-toggle]');
      btn?.setAttribute('aria-expanded', 'false');
    });
    openSlug = slug;
    const row = panel.closest('.svc-row');
    row?.classList.add('is-open');
    row?.querySelector('[data-service-toggle]')?.setAttribute('aria-expanded', 'true');
  });
})();
