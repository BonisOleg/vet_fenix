(() => {
  const decor = document.querySelector('.hero__decor[data-hero-decor="v2"]');
  if (!decor) {
    return;
  }

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const mobile = window.matchMedia('(max-width: 767px)').matches;

  if (reduceMotion || mobile) {
    return;
  }

  const hero = decor.closest('.hero');
  const items = decor.querySelectorAll('.hero__decor-item');
  if (!hero || !items.length) {
    return;
  }

  const VELOCITY_GAIN = 0.08;
  const MAX_BOOST = 4.5;
  const DECAY = 0.1;
  const PARALLAX_GAIN = 1.4;
  const WHEEL_GAIN = 0.004;
  const MAX_PARALLAX = 180;

  const itemState = Array.from(items, (el) => ({
    el,
    factor: Number.parseFloat(el.dataset.decorParallax) || 0.3,
    parallaxY: 0,
  }));

  let boost = 1;
  let targetBoost = 1;
  let lastScrollY = window.scrollY;
  let lastTime = performance.now();
  let rafId = null;
  let ticking = false;

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

  const applyScrollDelta = (deltaY) => {
    if (!deltaY) {
      return;
    }

    itemState.forEach((item) => {
      item.parallaxY = clamp(
        item.parallaxY + deltaY * item.factor * PARALLAX_GAIN,
        -MAX_PARALLAX,
        MAX_PARALLAX,
      );
    });
  };

  const updateVelocity = (deltaY, deltaTime) => {
    const velocity = Math.abs(deltaY) / Math.max(deltaTime, 16);
    targetBoost = clamp(1 + velocity * VELOCITY_GAIN, 1, MAX_BOOST);
  };

  const onScroll = () => {
    const now = performance.now();
    const deltaY = window.scrollY - lastScrollY;
    const deltaTime = now - lastTime;

    applyScrollDelta(deltaY);
    updateVelocity(deltaY, deltaTime);

    lastScrollY = window.scrollY;
    lastTime = now;
    ticking = false;
  };

  const requestScrollUpdate = () => {
    if (ticking) {
      return;
    }
    ticking = true;
    requestAnimationFrame(onScroll);
  };

  const onWheel = (event) => {
    const heroRect = hero.getBoundingClientRect();
    if (heroRect.bottom < 0 || heroRect.top > window.innerHeight) {
      return;
    }

    applyScrollDelta(event.deltaY * 0.35);
    targetBoost = clamp(targetBoost + Math.abs(event.deltaY) * WHEEL_GAIN, 1, MAX_BOOST);
  };

  const tick = () => {
    boost += (targetBoost - boost) * DECAY;
    targetBoost += (1 - targetBoost) * 0.04;

    decor.style.setProperty('--decor-speed-mult', boost.toFixed(3));

    itemState.forEach((item) => {
      item.parallaxY += (0 - item.parallaxY) * 0.03;
      item.el.style.setProperty('--decor-parallax-y', `${item.parallaxY.toFixed(2)}px`);
    });

    rafId = requestAnimationFrame(tick);
  };

  window.addEventListener('scroll', requestScrollUpdate, { passive: true });
  window.addEventListener('wheel', onWheel, { passive: true });

  lastScrollY = window.scrollY;
  lastTime = performance.now();
  rafId = requestAnimationFrame(tick);

  window.addEventListener(
    'pagehide',
    () => {
      window.removeEventListener('scroll', requestScrollUpdate);
      window.removeEventListener('wheel', onWheel);
      if (rafId !== null) {
        cancelAnimationFrame(rafId);
      }
    },
    { once: true },
  );
})();
