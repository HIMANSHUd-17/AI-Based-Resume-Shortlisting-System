/**
 * auth.js — sign in / sign up page.
 *  - animated sliding/cross-fade panel switch
 *  - inline validation errors that fade/slide in
 *  - submit button: loading pulse → success checkmark → fade to dashboard
 */
(() => {
  'use strict';

  const card = document.getElementById('auth-card');
  if (!card) return;

  const navigateTo = (window.ARS && window.ARS.navigateTo) || ((h) => { window.location.href = h; });

  const title = document.getElementById('auth-title');
  const subtitle = document.getElementById('auth-subtitle');
  const toggleText = document.getElementById('toggle-text');
  const toggleBtn = document.getElementById('toggle-btn');
  const signinPanel = document.getElementById('signin-panel');
  const signupPanel = document.getElementById('signup-panel');

  const STRINGS = {
    signin: {
      title: 'Welcome back',
      sub: 'Sign in to your account to continue',
      toggle: "Don't have an account?",
      btnLabel: 'Sign Up',
    },
    signup: {
      title: 'Create your account',
      sub: 'Start shortlisting resumes in under a minute',
      toggle: 'Already have an account?',
      btnLabel: 'Sign In',
    },
  };

  // server error key → input id, per panel
  const FIELD_MAP = {
    signin: { email: 'in-email', password: 'in-password' },
    signup: { name: 'up-name', email: 'up-email', password: 'up-password', confirm: 'up-confirm' },
  };

  // ── Panel switch ────────────────────────────────────────────────────────
  function setMode(mode) {
    card.dataset.mode = mode;
    const s = STRINGS[mode];
    title.textContent = s.title;
    subtitle.textContent = s.sub;
    toggleText.textContent = s.toggle;
    toggleBtn.textContent = s.btnLabel;
    history.replaceState(null, '', mode === 'signin' ? '/auth?mode=signin' : '/auth?mode=signup');
  }

  toggleBtn.addEventListener('click', () => {
    const next = card.dataset.mode === 'signin' ? 'signup' : 'signin';
    clearPanel(signinPanel);
    clearPanel(signupPanel);
    setMode(next);
  });

  // ── Field errors ────────────────────────────────────────────────────────
  function setFieldError(input, message) {
    const errEl = document.getElementById(`${input.id}-error`);
    if (message) {
      input.classList.add('field--error');
      errEl.textContent = message;
      errEl.hidden = false;
    } else {
      input.classList.remove('field--error');
      errEl.textContent = '';
      errEl.hidden = true;
    }
  }

  function clearPanel(panel) {
    panel.querySelectorAll('.field__input').forEach((input) => setFieldError(input, ''));
    const formErr = panel.querySelector('.auth-form__error');
    if (formErr) {
      formErr.textContent = '';
      formErr.hidden = true;
    }
  }

  function showFormError(panel, message) {
    const formErr = panel.querySelector('.auth-form__error');
    formErr.textContent = message;
    formErr.hidden = false;
  }

  // ── Client-side validation (returns {errors, values}) ───────────────────
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function validatePanel(mode) {
    const panel = mode === 'signin' ? signinPanel : signupPanel;
    const q = (id) => panel.querySelector(`#${id}`);
    const errors = {};
    const values = {};

    if (mode === 'signin') {
      const email = q('in-email').value.trim();
      const password = q('in-password').value;
      if (!EMAIL_RE.test(email)) errors.email = 'Please enter a valid email address.';
      if (!password) errors.password = 'Please enter your password.';
      values.email = email;
      values.password = password;
    } else {
      const name = q('up-name').value.trim();
      const email = q('up-email').value.trim();
      const password = q('up-password').value;
      const confirm = q('up-confirm').value;
      if (name.length < 2) errors.name = 'Please enter your full name.';
      if (!EMAIL_RE.test(email)) errors.email = 'Please enter a valid email address.';
      if (password.length < 6) errors.password = 'Password must be at least 6 characters.';
      if (confirm !== password) errors.confirm = 'Passwords do not match.';
      Object.assign(values, { name, email, password, confirm });
    }
    return { errors, values };
  }

  // ── Submit ──────────────────────────────────────────────────────────────
  function bindSubmit(panel, mode, endpoint) {
    panel.addEventListener('submit', async (e) => {
      e.preventDefault();
      const button = panel.querySelector('[data-js="auth-submit"]');
      if (button.classList.contains('is-loading') || button.classList.contains('is-success')) return;

      clearPanel(panel);
      const { errors, values } = validatePanel(mode);

      // show client errors inline (fade/slide in via CSS)
      if (Object.keys(errors).length) {
        Object.entries(errors).forEach(([key, msg]) => {
          const input = document.getElementById(FIELD_MAP[mode][key]);
          if (input) setFieldError(input, msg);
        });
        return;
      }

      // loading pulse
      button.classList.add('is-loading');
      button.disabled = true;

      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(values),
        });
        const data = await res.json();

        if (data.ok) {
          // success micro-interaction, then fade into the dashboard
          button.classList.remove('is-loading');
          button.classList.add('is-success');
          setTimeout(() => navigateTo(data.redirect || '/app'), 750);
          return;
        }

        button.classList.remove('is-loading');
        button.disabled = false;

        if (data.errors) {
          if (data.errors.form) {
            showFormError(panel, data.errors.form);
          }
          Object.entries(data.errors).forEach(([key, msg]) => {
            if (key === 'form') return;
            const input = document.getElementById(FIELD_MAP[mode][key]);
            if (input) setFieldError(input, msg);
          });
        } else if (data.error) {
          showFormError(panel, data.error);
        }
      } catch {
        button.classList.remove('is-loading');
        button.disabled = false;
        showFormError(panel, 'Something went wrong. Please try again.');
      }
    });
  }

  // ── Init ────────────────────────────────────────────────────────────────
  setMode(card.dataset.mode === 'signup' ? 'signup' : 'signin');
  bindSubmit(signinPanel, 'signin', '/auth/login');
  bindSubmit(signupPanel, 'signup', '/auth/signup');
})();
