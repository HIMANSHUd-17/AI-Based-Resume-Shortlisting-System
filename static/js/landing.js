/**
 * landing.js — landing page animations.
 *  - hero: heading / subtext / CTA slide up in a 100ms-staggered sequence
 *    (hero CTA pops in via the CSS `cta-in` keyframe — same ease-out language
 *    as everything else entering the screen)
 *
 * Everything respects prefers-reduced-motion (elements appear instantly).
 */
(() => {
  'use strict';

  const reduceMotion = (window.ARS && window.ARS.reduceMotion) || false;
  const hasGSAP = typeof window.gsap !== 'undefined';
  const hasObserver = 'IntersectionObserver' in window;

  function runWhenReady(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  // ── Hero staggered entrance ─────────────────────────────────────────────
  function initHero() {
    const els = Array.from(document.querySelectorAll('[data-hero]'));
    if (!els.length) return;

    if (reduceMotion || !hasGSAP) {
      els.forEach((el) => {
        el.style.opacity = 1;
        el.style.transform = 'none';
      });
      return;
    }

    // 100ms stagger, ease-out; CSS (html.js) keeps them hidden until here.
    // The hero CTA pops in separately via the CSS `cta-in` animation.
    gsap.fromTo(
      els,
      { opacity: 0, y: 28 },
      { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out', stagger: 0.1, delay: 0.15 }
    );
  }

  runWhenReady(() => {
    initHero();
  });
})();
