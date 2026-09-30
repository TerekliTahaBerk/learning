(() => {
  const body = document.body;
  const page = body.dataset.page || 'index.html';
  const root = body.dataset.root || '.';
  const themeKey = 'learning-theme';
  const setTheme = theme => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem(themeKey, theme); } catch (_) {}
  };
  try { const saved = localStorage.getItem(themeKey); if (saved) setTheme(saved); } catch (_) {}
  document.querySelector('[data-action="theme"]')?.addEventListener('click', () =>
    setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));

  const menuButton = document.querySelector('[data-action="menu"]');
  const closeMenu = () => { body.classList.remove('menu-open'); menuButton?.setAttribute('aria-expanded', 'false'); };
  menuButton?.addEventListener('click', () => { const open = body.classList.toggle('menu-open'); menuButton.setAttribute('aria-expanded', String(open)); });
  document.querySelector('[data-action="close-menu"]')?.addEventListener('click', closeMenu);
  document.querySelectorAll('.sidebar a').forEach(a => a.addEventListener('click', closeMenu));

  const outline = document.getElementById('on-this-page');
  const article = document.getElementById('article');
  if (outline && article) {
    article.querySelectorAll('h2, h3').forEach((heading, i) => {
      if (!heading.id) heading.id = `section-${i+1}`;
      const anchor = document.createElement('a');
      anchor.href = `#${heading.id}`;
      anchor.textContent = heading.textContent;
      if (heading.tagName === 'H3') anchor.style.paddingLeft = '20px';
      outline.append(anchor);
    });
    if (!outline.children.length) outline.innerHTML = '<span style="font-size:11px;color:var(--muted)">Bu sayfada bölüm başlığı yok.</span>';
  }

  const progress = document.getElementById('read-progress');
  const progressLabel = document.getElementById('progress-label');
  const updateProgress = () => {
    if (!progress) return;
    const total = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const pct = Math.min(100, Math.max(0, Math.round(scrollY / total * 100)));
    progress.style.width = `${pct}%`;
    progressLabel.textContent = `%${pct}`;
  };
  addEventListener('scroll', updateProgress, {passive:true});
  addEventListener('resize', updateProgress, {passive:true});
  updateProgress();
  const readButton = document.querySelector('[data-action="mark-read"]');
  const readKey = `learning-read:${page}`;
  const syncRead = () => {
    let read = false;
    try { read = localStorage.getItem(readKey) === '1'; } catch (_) {}
    if (readButton) { readButton.classList.toggle('is-read', read); readButton.textContent = read ? 'Okundu ✓' : 'Okudum olarak işaretle'; }
  };
  readButton?.addEventListener('click', () => { try { localStorage.setItem(readKey, localStorage.getItem(readKey) === '1' ? '0' : '1'); } catch (_) {} syncRead(); });
  syncRead();

  const dialog = document.getElementById('search-dialog');
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  let entries;
  const normalize = s => String(s || '').toLocaleLowerCase('tr');
  async function loadEntries() {
    if (entries) return entries;
    const response = await fetch(body.dataset.search);
    if (!response.ok) throw new Error('Search index unavailable');
    entries = await response.json();
    return entries;
  }
  const showMessage = message => { results.replaceChildren(); const p = document.createElement('p'); p.textContent = message; results.append(p); };
  async function search(query) {
    const value = normalize(query.trim());
    if (!value) { showMessage('İspanyolca ve AI Engineering sayfalarında ara.'); return; }
    try {
      const all = await loadEntries();
      const terms = value.split(/\s+/).filter(Boolean);
      const found = all.map(entry => {
        const title = normalize(entry.title), text = normalize(entry.text);
        const score = terms.every(term => title.includes(term) || text.includes(term))
          ? terms.reduce((sum, term) => sum + (title.includes(term) ? 5 : 1), 0) : 0;
        return {entry, score};
      }).filter(item => item.score).sort((a,b) => b.score-a.score).slice(0,30);
      results.replaceChildren();
      if (!found.length) { showMessage('Eşleşen sayfa bulunamadı. Farklı bir kelime dene.'); return; }
      found.forEach(({entry}) => {
        const a = document.createElement('a'); a.className = 'search-result';
        a.href = `${root}/${entry.path}`;
        const book = document.createElement('small'); book.textContent = entry.book;
        const title = document.createElement('strong'); title.textContent = entry.title;
        const excerpt = document.createElement('span'); excerpt.textContent = entry.text.slice(0,180);
        a.append(book,title,excerpt); results.append(a);
      });
    } catch (_) { showMessage('Arama dizini yüklenemedi. Sayfayı yeniden açıp tekrar dene.'); }
  }
  const openSearch = () => { dialog.showModal(); input.value = ''; search(''); input.focus(); };
  document.querySelector('[data-action="search"]')?.addEventListener('click', openSearch);
  document.querySelector('[data-action="close-search"]')?.addEventListener('click', () => dialog.close());
  input?.addEventListener('input', () => search(input.value));
  addEventListener('keydown', event => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); openSearch(); }
    if (event.key === 'Escape') closeMenu();
  });
})();
