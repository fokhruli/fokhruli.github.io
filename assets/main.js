/* ════════════════════════════════════════════════════════════════════
   main.js — shared across all pages
   ════════════════════════════════════════════════════════════════════ */

/* ── Scroll progress bar ──────────────────────────────────────────── */
(function () {
  const bar = document.getElementById('progress-bar');
  if (!bar) return;
  function updateBar() {
    const scrolled = window.scrollY;
    const total = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = total > 0 ? (scrolled / total * 100) + '%' : '0%';
  }
  window.addEventListener('scroll', updateBar, { passive: true });
  updateBar();
})();

/* ── Search data ─────────────────────────────────────────────────── */
const SEARCH_DATA = [
  // Pages
  { title: 'About',           url: '/',                        icon: 'fa-user',        section: 'Pages' },
  { title: 'Blog',            url: '/blog/',                   icon: 'fa-pen-nib',     section: 'Pages' },
  { title: 'Publications',    url: '/publications.html',       icon: 'fa-scroll',      section: 'Pages' },
  { title: 'Media Coverage',  url: '/media.html',              icon: 'fa-newspaper',   section: 'Pages' },
  { title: 'Talks',           url: '/talks.html',              icon: 'fa-microphone',  section: 'Pages' },
  { title: 'CV (PDF)',        url: '/files/cv.pdf',            icon: 'fa-file-pdf',    section: 'Pages' },
  // Publications
  { title: 'ReKon3D — Neurocomputing 2025',           url: 'https://www.sciencedirect.com/science/article/pii/S0925231225009361', icon: 'fa-file-alt', section: 'Publications' },
  { title: 'VAE-GAN3D — Image & Vision Computing 2024', url: 'https://www.sciencedirect.com/science/article/abs/pii/S0262885624001537', icon: 'fa-file-alt', section: 'Publications' },
  { title: 'Bangla-English Code-Mixed SA — IEEE Access 2023', url: 'https://ieeexplore.ieee.org/abstract/document/10129187', icon: 'fa-file-alt', section: 'Publications' },
  { title: 'AI-driven Stroke Rehabilitation Review — IEEE TNSRE 2022', url: 'https://ieeexplore.ieee.org/document/9936658', icon: 'fa-file-alt', section: 'Publications' },
  { title: 'GCN for Rehab Exercise Assessment — IEEE TNSRE 2022', url: 'https://ieeexplore.ieee.org/document/9709340', icon: 'fa-file-alt', section: 'Publications' },
  // Project pages
  { title: 'STGCN-Rehab project page',       url: '/STGCN-rehab/',        icon: 'fa-link', section: 'Projects' },
  { title: 'CM-Senti-Analysis project page', url: '/CM-senti-analysis/',  icon: 'fa-link', section: 'Projects' },
  // Social
  { title: 'GitHub',        url: 'https://github.com/fokhruli',       icon: 'fab fa-github',   section: 'Links' },
  { title: 'Google Scholar', url: 'https://scholar.google.com/citations?user=bQjPde8AAAAJ', icon: 'ai ai-google-scholar', section: 'Links' },
  { title: 'Twitter / X',  url: 'https://twitter.com/fokhrul_i',      icon: 'fab fa-twitter',  section: 'Links' },
];

/* ── Search overlay ─────────────────────────────────────────────── */
(function () {
  const overlay = document.getElementById('search-overlay');
  const input   = document.getElementById('search-input');
  const list    = document.getElementById('search-results');
  if (!overlay || !input || !list) return;

  let activeIdx = -1;

  function open() {
    overlay.classList.add('open');
    input.value = '';
    render('');
    setTimeout(() => input.focus(), 50);
  }

  function close() {
    overlay.classList.remove('open');
    activeIdx = -1;
  }

  function render(query) {
    const q = query.trim().toLowerCase();
    const results = q
      ? SEARCH_DATA.filter(d => d.title.toLowerCase().includes(q) || d.section.toLowerCase().includes(q))
      : SEARCH_DATA.slice(0, 8);

    list.innerHTML = results.map((r, i) => `
      <li class="${i === activeIdx ? 'active' : ''}">
        <a href="${r.url}" ${r.url.startsWith('http') ? 'target="_blank" rel="noopener"' : ''}>
          <span class="result-icon"><i class="${r.icon.startsWith('fa') ? r.icon.includes(' ') ? r.icon : 'fas ' + r.icon : r.icon}"></i></span>
          <span>${r.title}</span>
          <span class="result-section">${r.section}</span>
        </a>
      </li>`).join('');

    activeIdx = -1;
  }

  function navigate(dir) {
    const items = list.querySelectorAll('li');
    if (!items.length) return;
    items[Math.max(0, activeIdx)]?.classList.remove('active');
    activeIdx = Math.min(Math.max(activeIdx + dir, 0), items.length - 1);
    items[activeIdx]?.classList.add('active');
    items[activeIdx]?.scrollIntoView({ block: 'nearest' });
  }

  function confirmActive() {
    const active = list.querySelector('li.active a');
    if (active) { active.click(); close(); }
  }

  // Triggers
  const btn = document.getElementById('search-trigger');
  if (btn) btn.addEventListener('click', open);

  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); open(); return; }
    if (!overlay.classList.contains('open')) return;
    if (e.key === 'Escape') { close(); return; }
    if (e.key === 'ArrowDown') { e.preventDefault(); navigate(1); return; }
    if (e.key === 'ArrowUp')   { e.preventDefault(); navigate(-1); return; }
    if (e.key === 'Enter')     { confirmActive(); return; }
  });

  overlay.addEventListener('click', e => { if (e.target === overlay) close(); });
  input.addEventListener('input', () => render(input.value));
})();
