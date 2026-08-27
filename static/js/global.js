/**
 * global.js — shared behaviour across all three pages.
 *  - prefers-reduced-motion flag (exposed on window.ARS)
 *  - page enter/leave transitions (no hard snaps between pages)
 *  - sticky navbar shrink on scroll
 *  - scroll-reveal via IntersectionObserver
 *  - user avatar dropdown + logout (dashboard nav)
 */
(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasObserver = 'IntersectionObserver' in window;
  window.ARS = window.ARS || {};

  // Mark that JS is active — CSS uses `html.js` to enable hidden states,
  // so content stays visible if scripts are disabled.
  document.documentElement.classList.add('js');

  // ── Page transitions ────────────────────────────────────────────────────
  // Wait out the full CSS page-leave animation (`--t-page: 360ms`) so the
  // fade completes before navigation — cutting it short looks like a snap.
  const PAGE_LEAVE_MS = 360;

  function navigateTo(href) {
    if (reduceMotion) {
      window.location.href = href;
      return;
    }
    document.body.classList.remove('page-enter');
    document.body.classList.add('page-leave');
    setTimeout(() => { window.location.href = href; }, PAGE_LEAVE_MS);
  }
  window.ARS.navigateTo = navigateTo;

  // Intercept internal link clicks → fade out → navigate.
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href]');
    if (!link) return;
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('//')) return;
    if (!href.startsWith('/')) return; // external / mailto etc.
    if (link.target === '_blank' || link.hasAttribute('download')) return;
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    navigateTo(href);
  });

  // ── Navbar shrink on scroll ──────────────────────────────────────────────
  const nav = document.getElementById('site-nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 12);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // ── Scroll reveal (generic .reveal elements) ────────────────────────────
  const revealEls = Array.from(document.querySelectorAll('.reveal'));
  const reveal = (el) => el.classList.add('is-visible');

  if (reduceMotion || !hasObserver) {
    revealEls.forEach(reveal);
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            reveal(entry.target);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach((el) => io.observe(el));
  }

  // ── User avatar dropdown (dashboard) ────────────────────────────────────
  const menu = document.getElementById('user-menu');
  if (menu) {
    const trigger = menu.querySelector('[data-js="user-menu-trigger"]');
    const setOpen = (open) => {
      menu.classList.toggle('open', open);
      trigger.setAttribute('aria-expanded', String(open));
    };
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      setOpen(!menu.classList.contains('open'));
    });
    document.addEventListener('click', () => setOpen(false));
  }

  // ── Logout ──────────────────────────────────────────────────────────────
  const logoutBtn = document.querySelector('[data-js="logout-btn"]');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      try {
        const res = await fetch('/auth/logout', { method: 'POST' });
        const data = await res.json().catch(() => ({}));
        navigateTo(data.redirect || '/');
      } catch {
        navigateTo('/');
      }
    });
  }
})();
