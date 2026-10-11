
/**
 * app.js — dashboard (the working tool).
 *  - drag-and-drop resume upload with hover + pop micro-interactions
 *  - file chips (add / remove)
 *  - Run Match → POST /api/match with a skeleton loading state
 *  - results revealed with a staggered fade/slide-in (score → breakdown → skills)
 *
 * All resume-derived strings (names, filenames, skills) are rendered with
 * textContent, never innerHTML, to avoid HTML injection from uploaded files.
 */
(() => {
  'use strict';

  const reduceMotion = (window.ARS && window.ARS.reduceMotion) || false;
  const jdText = document.getElementById('jd-text');
  const jdError = document.getElementById('jd-error');
  const fileInput = document.getElementById('file-input');
  const dropzone = document.getElementById('dropzone');
  const fileListEl = document.getElementById('file-list');
  const filesError = document.getElementById('files-error');
  const skillInput = document.getElementById('skill-input');
  const skillChips = document.getElementById('skill-chips');
  const skillStatus = document.getElementById('skill-status');
  const addSkillBtn = document.getElementById('add-skill');
  const skillCatalogEl = document.getElementById('skill-catalog');
  const runBtn = document.getElementById('run-match');
  const downloadBtn = document.getElementById('download-csv');
  const candidateLimit = document.getElementById('candidate-limit');
  const runHint = document.getElementById('run-hint');
  const resultsEl = document.getElementById('results');

  if (!jdText || !dropzone || !runBtn || !resultsEl) return;

  const MAX_FILE_BYTES = 5 * 1024 * 1024;
  const RING_CIRCUMFERENCE = 264; // 2π · r(42)
  let files = []; // File[]
  let selectedSkills = [];
  let latestResults = [];
  const skillCatalog = skillCatalogEl ? JSON.parse(skillCatalogEl.textContent) : [];

  // ── Helpers ─────────────────────────────────────────────────────────────
  function showError(el, message) {
    el.textContent = message;
    el.hidden = false;
  }
  function hideError(el) {
    el.textContent = '';
    el.hidden = true;
  }
  function fmtSize(bytes) {
    return bytes >= 1024 * 1024
      ? `${(bytes / (1024 * 1024)).toFixed(1)} MB`
      : `${Math.round(bytes / 1024)} KB`;
  }
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function updateRunState() {
    const ready = jdText.value.trim().length > 0 && files.length > 0;
    runBtn.disabled = !ready;
    runHint.textContent = ready
      ? `Ready to match ${files.length} resume${files.length > 1 ? 's' : ''}.`
      : 'Add a job description and at least one resume to enable the match.';
  }

  function detectSkills(text) {
    return skillCatalog.filter((skill) => {
      const escaped = skill.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const simpleSkill = /^[a-z0-9]+$/i.test(skill);
      return simpleSkill
        ? new RegExp(`\\b${escaped}\\b`, 'i').test(text)
        : text.toLowerCase().includes(skill.toLowerCase());
    });
  }

  function renderSkillChips() {
    skillChips.textContent = '';
    if (!selectedSkills.length) {
      skillChips.appendChild(el('span', 'skill-picker__empty', 'Skills will appear as you type.'));
      skillStatus.textContent = 'Detected from your job description';
      return;
    }

    skillStatus.textContent = `${selectedSkills.length} skill${selectedSkills.length === 1 ? '' : 's'} selected`;
    selectedSkills.forEach((skill) => {
      const chip = el('button', 'skill-chip', skill);
      chip.type = 'button';
      chip.title = `Remove ${skill}`;
      chip.addEventListener('click', () => {
        selectedSkills = selectedSkills.filter((item) => item !== skill);
        renderSkillChips();
      });
      skillChips.appendChild(chip);
    });
  }

  function syncDetectedSkills() {
    const detected = detectSkills(jdText.value);
    selectedSkills = [...new Set([...selectedSkills, ...detected])];
    renderSkillChips();
  }

  function addSkill() {
    const value = skillInput.value.trim().toLowerCase();
    const skill = skillCatalog.find((item) => item.toLowerCase() === value);
    if (skill && !selectedSkills.includes(skill)) selectedSkills.push(skill);
    skillInput.value = '';
    renderSkillChips();
  }

  // ── File collection ─────────────────────────────────────────────────────
  function addFiles(fileList) {
    const badTypes = [];
    const tooLarge = [];
    Array.from(fileList).forEach((f) => {
      const ext = f.name.split('.').pop().toLowerCase();
      if (!['pdf', 'docx'].includes(ext)) {
        badTypes.push(f.name);
        return;
      }
      if (f.size > MAX_FILE_BYTES) {
        tooLarge.push(f.name);
        return;
      }
      if (!files.some((existing) => existing.name === f.name && existing.size === f.size)) {
        files.push(f);
      }
    });

    if (badTypes.length || tooLarge.length) {
      const parts = [];
      if (badTypes.length) parts.push(`Only PDF/DOCX allowed (${badTypes[0]}${badTypes.length > 1 ? ` +${badTypes.length - 1}` : ''}).`);
      if (tooLarge.length) parts.push(`Max 5 MB per file (${tooLarge[0]}${tooLarge.length > 1 ? ` +${tooLarge.length - 1}` : ''}).`);
      showError(filesError, parts.join(' '));
    } else {
      hideError(filesError);
    }

    if (files.length) {
      dropzone.classList.remove('is-pop');
      void dropzone.offsetWidth; // restart the animation
      dropzone.classList.add('is-pop');
    }

    renderFileList();
    updateRunState();
  }

  function renderFileList() {
    fileListEl.textContent = '';
    files.forEach((f, i) => {
      const chip = el('li', 'file-chip');
      const icon = el('span', 'file-chip__icon', '📄');
      const name = el('span', 'file-chip__name', f.name);
      name.title = f.name;
      const size = el('span', 'file-chip__size', fmtSize(f.size));
      const remove = el('button', 'file-chip__remove', '×');
      remove.type = 'button';
      remove.setAttribute('aria-label', `Remove ${f.name}`);
      remove.addEventListener('click', () => {
        files.splice(i, 1);
        renderFileList();
        updateRunState();
      });
      chip.append(icon, name, size, remove);
      fileListEl.appendChild(chip);
    });
  }

  // drag & drop + click to browse
  dropzone.addEventListener('click', () => fileInput.click());
  dropzone.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });
  ['dragover', 'dragenter'].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.add('is-dragover');
    });
  });
  ['dragleave', 'drop'].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.remove('is-dragover');
    });
  });
  dropzone.addEventListener('drop', (e) => addFiles(e.dataTransfer.files));
  fileInput.addEventListener('change', () => {
    addFiles(fileInput.files);
    fileInput.value = ''; // allow re-selecting the same file
  });

  // ── Run match ───────────────────────────────────────────────────────────
  jdText.addEventListener('input', () => {
    hideError(jdError);
    jdText.classList.remove('field--error');
    syncDetectedSkills();
    updateRunState();
  });
  addSkillBtn.addEventListener('click', addSkill);
  skillInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      addSkill();
    }
  });

  function renderSkeleton() {
    resultsEl.textContent = '';
    const grid = el('div', 'skeleton-grid');
    for (let i = 0; i < 3; i++) {
      const card = el('div', 'skeleton-card');
      const line = (cls) => el('div', `skeleton__line ${cls}`.trim());
      card.append(
        line('skeleton__line--title'),
        line(''),
        line('skeleton__line--short'),
        line('skeleton__line--lg'),
        line('skeleton__line--lg')
      );
      grid.appendChild(card);
    }
    resultsEl.appendChild(grid);
    resultsEl.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
  }

  function showResultsError(message) {
    resultsEl.textContent = '';
    const box = el('div', 'results-empty');
    const emoji = el('div', 'emoji', '⚠️');
    const msg = el('p', '', message);
    box.append(emoji, msg);
    resultsEl.appendChild(box);
  }

  function csvCell(value) {
    const text = Array.isArray(value) ? value.join(' | ') : String(value ?? '');
    return `"${text.replace(/"/g, '""')}"`;
  }

  function downloadCsv() {
    if (!latestResults.length) return;

    const headers = [
      'Rank', 'Candidate Name', 'Resume Filename', 'Final Score',
      'Skill Match', 'TF-IDF Relevance', 'Experience (Years)', 'Education',
      'Skills Found', 'Skills Missing',
    ];
    const rows = latestResults.map((candidate) => [
      candidate.rank,
      candidate.name,
      candidate.filename,
      `${pct(candidate.final_score)}%`,
      `${pct(candidate.skill_match_pct)}%`,
      `${pct(candidate.tfidf_score)}%`,
      candidate.experience_years,
      candidate.education,
      candidate.skills_found,
      candidate.skills_missing,
    ]);
    const csv = [headers, ...rows].map((row) => row.map(csvCell).join(',')).join('\r\n');
    const blob = new Blob([`\uFEFF${csv}`], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `resume-shortlist-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  // ── Result rendering ────────────────────────────────────────────────────
  function pct(value) {
    return Math.round((value || 0) * 100);
  }

  function buildRing(score, idSuffix) {
    const wrap = el('div', 'score-ring');
    const svgNS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(svgNS, 'svg');
    svg.setAttribute('width', '92');
    svg.setAttribute('height', '92');
    svg.setAttribute('viewBox', '0 0 92 92');
    svg.innerHTML =
      `<defs><linearGradient id="scoreGradient-${idSuffix}" x1="0%" y1="0%" x2="100%" y2="100%">` +
      `<stop offset="0%" stop-color="#6366f1"/><stop offset="100%" stop-color="#a78bfa"/>` +
      `</linearGradient></defs>`;
    const track = document.createElementNS(svgNS, 'circle');
    track.setAttribute('class', 'score-ring__track');
    track.setAttribute('cx', '46'); track.setAttribute('cy', '46'); track.setAttribute('r', '42');
    const value = document.createElementNS(svgNS, 'circle');
    value.setAttribute('class', 'score-ring__value');
    value.setAttribute('cx', '46'); value.setAttribute('cy', '46'); value.setAttribute('r', '42');
    value.setAttribute('style', `stroke:url(#scoreGradient-${idSuffix})`);
    value.dataset.offset = String(RING_CIRCUMFERENCE * (1 - score));
    svg.append(track, value);

    const label = el('div', 'score-ring__label');
    label.append(el('strong', '', `${pct(score)}%`), el('span', '', 'match'));

    wrap.append(svg, label);
    return wrap;
  }

  function buildSummary(data) {
    const top = data.results[0];
    const row = el('div', 'result-row results__summary');
    const left = el('div', 'summary-top');
    const names = el('ol', 'summary-candidates');
    data.results.forEach((candidate) => {
      const item = el('li', '', `#${candidate.rank} ${candidate.name}`);
      names.appendChild(item);
    });
    left.append(
      el('p', 'summary-label', `Best ${data.results.length} match${data.results.length === 1 ? '' : 'es'}`),
      el('h3', 'summary-name', 'Selected candidates'),
      names,
      el(
        'p',
        'summary-meta',
        `Top score: ${pct(top.final_score)}% · ${top.experience_years ? `${top.experience_years} yr${top.experience_years > 1 ? 's' : ''} experience` : 'Fresher'} · ${top.education}`
      ),
      el('span', 'summary-badge', `${data.results.length} candidate${data.results.length === 1 ? '' : 's'} selected`)
    );
    row.append(left, buildRing(top.final_score, 'top'));
    return row;
  }

  function buildCandidate(c, idSuffix) {
    const card = el('article', 'result-row candidate-card');

    const body = el('div', 'candidate-card__body');
    const head = el('div', 'candidate-card__head');
    head.append(
      el('span', 'candidate-card__rank', `#${c.rank}`),
      el('h3', 'candidate-card__name', c.name)
    );
    body.appendChild(head);

    const meta = el('div', 'candidate-card__meta');
    meta.append(
      el('span', 'meta-chip', `🎓 ${c.education}`),
      el('span', 'meta-chip', `💼 ${c.experience_years ? `${c.experience_years} yr${c.experience_years > 1 ? 's' : ''}` : 'Fresher'}`)
    );
    body.appendChild(meta);

    // breakdown bars
    const breakdown = el('div', 'breakdown');
    const items = [
      { label: 'Skill match', value: c.skill_match_pct },
      { label: 'TF-IDF relevance', value: c.tfidf_score, alt: true },
    ];
    items.forEach((item) => {
      const wrap = el('div', 'breakdown__item');
      const row = el('div', 'breakdown__row');
      row.append(el('span', '', item.label), el('span', '', `${pct(item.value)}%`));
      const bar = el('div', 'breakdown__bar');
      const fill = el('div', `breakdown__fill${item.alt ? ' breakdown__fill--alt' : ''}`);
      fill.dataset.pct = String(pct(item.value));
      fill.style.width = '0';
      bar.appendChild(fill);
      wrap.append(row, bar);
      breakdown.appendChild(wrap);
    });
    body.appendChild(breakdown);

    // skills found / missing
    const chips = (list, cls, label) => {
      const wrap = el('div', 'skills-block');
      wrap.appendChild(el('h4', '', `${label} (${list.length})`));
      const container = el('div', 'skills-block__chips');
      const initialCount = 14;
      const render = (expanded) => {
        container.textContent = '';
        const shown = expanded ? list : list.slice(0, initialCount);
        shown.forEach((s) => container.appendChild(el('span', `tag ${cls}`, s)));
        if (list.length > initialCount) {
          const toggle = el('button', 'tag tag--toggle', expanded ? 'Show less' : `+${list.length - initialCount} more`);
          toggle.type = 'button';
          toggle.addEventListener('click', () => render(!expanded));
          container.appendChild(toggle);
        }
      };
      render(false);
      wrap.appendChild(container);
      return wrap;
    };

    if (c.skills_found.length) body.appendChild(chips(c.skills_found, 'tag--found', 'Skills found'));
    if (c.skills_missing.length) {
      const wrap = el('div', 'skills-block');
      wrap.appendChild(el('h4', '', 'Skills missing'));
      const container = el('div', 'skills-block__chips');
      const initialCount = 10;
      const render = (expanded) => {
        container.textContent = '';
        const shown = expanded ? c.skills_missing : c.skills_missing.slice(0, initialCount);
        shown.forEach((s) => container.appendChild(el('span', 'tag tag--missing', s)));
        if (c.skills_missing.length > initialCount) {
          const toggle = el('button', 'tag tag--missing tag--toggle', expanded ? 'Show less' : `+${c.skills_missing.length - initialCount} more`);
          toggle.type = 'button';
          toggle.addEventListener('click', () => render(!expanded));
          container.appendChild(toggle);
        }
      };
      render(false);
      wrap.appendChild(container);
      body.appendChild(wrap);
    }

    card.append(buildRing(c.final_score, idSuffix), body);
    return card;
  }

  function renderResults(data) {
    resultsEl.textContent = '';
    const frag = document.createDocumentFragment();
    frag.appendChild(buildSummary(data));

    const list = el('div', 'candidates');
    data.results.forEach((c, i) => list.appendChild(buildCandidate(c, `c${i}`)));
    frag.appendChild(list);
    resultsEl.appendChild(frag);

    revealRows(resultsEl);
  }

  // staggered fade/slide-in; then draw bars + rings
  function revealRows(container) {
    const rows = Array.from(container.querySelectorAll('.result-row'));
    rows.forEach((row, i) => {
      if (i > 0) row.style.transitionDelay = `${i * 90}ms`;
      void row.offsetWidth; // force reflow so the transition starts cleanly
      row.classList.add('row-in');
      setTimeout(() => {
        row.querySelectorAll('.breakdown__fill').forEach((fill) => {
          fill.style.width = `${fill.dataset.pct}%`;
        });
        row.querySelectorAll('.score-ring__value').forEach((ring) => {
          ring.style.strokeDashoffset = ring.dataset.offset;
        });
      }, reduceMotion ? 0 : 60 + i * 90);
    });
  }

  runBtn.addEventListener('click', async () => {
    const jd = jdText.value.trim();
    if (!jd) {
      showError(jdError, 'Please paste a job description first.');
      jdText.classList.add('field--error');
      return;
    }
    if (!files.length) {
      showError(filesError, 'Please add at least one resume.');
      return;
    }
    hideError(jdError);
    hideError(filesError);
    latestResults = [];
    downloadBtn.disabled = true;

    runBtn.classList.add('is-loading');
    renderSkeleton();

    try {
      const formData = new FormData();
      formData.append('job_description', jd);
      formData.append('skills', JSON.stringify(selectedSkills));
      formData.append('candidate_limit', candidateLimit.value);
      files.forEach((f) => formData.append('files', f, f.name));

      const res = await fetch('/api/match', { method: 'POST', body: formData });
      const data = await res.json();

      if (data.ok) {
        latestResults = data.results;
        downloadBtn.disabled = false;
        renderResults(data);
      } else {
        showResultsError(data.error || 'The match could not be completed. Please try again.');
      }
    } catch {
      showResultsError('Network error — please check the server and try again.');
    } finally {
      runBtn.classList.remove('is-loading');
      updateRunState();
    }
  });
  downloadBtn.addEventListener('click', downloadCsv);

  // ── Init ────────────────────────────────────────────────────────────────
  updateRunState();
})();
