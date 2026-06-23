(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealEls = document.querySelectorAll('[data-reveal]');
  const countEls = document.querySelectorAll('[data-count]');

  if (!revealEls.length && !countEls.length) {
    return;
  }

  const revealAll = () => {
    revealEls.forEach((el) => {
      el.classList.add('is-revealed');
    });
  };

  const COUNT_DURATION_MS = 1800;
  const isMobile = window.matchMedia('(max-width: 767px)').matches;
  const observerOptions = isMobile
    ? { rootMargin: '0px 0px -2% 0px', threshold: 0.06 }
    : { rootMargin: '0px 0px -10% 0px', threshold: 0.15 };

  const easeOutCubic = (t) => 1 - (1 - t) ** 3;

  const parseCount = (el) => {
    const raw = (el.textContent || '').trim();
    const match = raw.match(/^(\d+)(.*)$/);
    if (!match) {
      return null;
    }
    return {
      target: Number.parseInt(match[1], 10),
      suffix: match[2],
    };
  };

  const animateCount = (el) => {
    if (el.dataset.countDone === '1') {
      return;
    }

    const parsed = parseCount(el);
    if (!parsed || parsed.target <= 0) {
      return;
    }

    el.dataset.countDone = '1';
    const { target, suffix } = parsed;
    const start = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - start) / COUNT_DURATION_MS, 1);
      const value = Math.round(easeOutCubic(progress) * target);
      el.textContent = `${value}${suffix}`;
      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    };

    el.textContent = `0${suffix}`;
    requestAnimationFrame(tick);
  };

  if (reduceMotion) {
    revealAll();
    countEls.forEach((el) => {
      el.dataset.countDone = '1';
    });
    return;
  }

  if (revealEls.length) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        entry.target.classList.add('is-revealed');
        revealObserver.unobserve(entry.target);
      });
    }, observerOptions);

    revealEls.forEach((el) => {
      revealObserver.observe(el);
    });
  }

  if (countEls.length) {
    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        animateCount(entry.target);
        countObserver.unobserve(entry.target);
      });
    }, observerOptions);

    countEls.forEach((el) => {
      countObserver.observe(el);
    });
  }
})();
