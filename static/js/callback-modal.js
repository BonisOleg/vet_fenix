(() => {
  const modal = document.getElementById('callback-modal');
  if (!modal) {
    return;
  }

  const TIMER_MS = 30000;
  const STORAGE_START = 'callbackModalStart';
  const STORAGE_SHOWN = 'callbackModalShown';
  const root = document.getElementById('callback-modal-root');
  let timerId = null;

  const markShown = () => {
    sessionStorage.setItem(STORAGE_SHOWN, '1');
    if (timerId !== null) {
      window.clearTimeout(timerId);
      timerId = null;
    }
  };

  const openModal = () => {
    if (sessionStorage.getItem(STORAGE_SHOWN)) {
      return;
    }
    modal.hidden = false;
    document.body.classList.add('callback-modal-open');
    window.requestAnimationFrame(() => {
      window.requestAnimationFrame(() => {
        modal.classList.add('is-open');
      });
    });
    window.setTimeout(() => {
      const firstInput = modal.querySelector('.field-input, .field-select');
      firstInput?.focus({ preventScroll: true });
    }, 420);
    markShown();
  };

  const closeModal = () => {
    modal.classList.remove('is-open');
    document.body.classList.remove('callback-modal-open');
    window.setTimeout(() => {
      if (!modal.classList.contains('is-open')) {
        modal.hidden = true;
      }
    }, 500);
    markShown();
  };

  const scheduleOpen = () => {
    if (sessionStorage.getItem(STORAGE_SHOWN)) {
      return;
    }

    const storedStart = sessionStorage.getItem(STORAGE_START);
    const start = storedStart ? Number.parseInt(storedStart, 10) : Date.now();
    if (!storedStart) {
      sessionStorage.setItem(STORAGE_START, String(start));
    }

    const remaining = Math.max(0, TIMER_MS - (Date.now() - start));
    timerId = window.setTimeout(openModal, remaining);
  };

  document.querySelectorAll('[data-callback-close]').forEach((el) => {
    el.addEventListener('click', closeModal);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modal.classList.contains('is-open')) {
      closeModal();
    }
  });

  root?.addEventListener('htmx:afterSwap', () => {
    if (root.querySelector('.callback-modal__success')) {
      markShown();
    }
  });

  scheduleOpen();
})();
