(() => {
  'use strict';
  const posts = JSON.parse(document.getElementById('post-data').textContent);
  const form = document.getElementById('filters');
  const search = document.getElementById('search');
  const topic = document.getElementById('topic');
  const year = document.getElementById('year');
  const list = document.getElementById('posts');
  const pager = document.getElementById('pagination');
  const count = document.getElementById('result-count');
  const pageSize = 15;
  let page = 1;
  const escape = value => value.replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  function readURL() {
    const params = new URLSearchParams(location.search);
    search.value = params.get('q') || '';
    topic.value = params.get('topic') || '';
    year.value = params.get('year') || '';
    page = Math.max(1, Number.parseInt(params.get('page'), 10) || 1);
  }
  function render() {
    const query = search.value.trim().toLowerCase();
    const filtered = posts.filter(p => (!topic.value || p.topic === topic.value) && (!year.value || p.date.startsWith(year.value)) && (!query || `${p.title} ${p.description} ${p.topic}`.toLowerCase().includes(query)));
    const pages = Math.max(1, Math.ceil(filtered.length / pageSize));
    page = Math.min(page, pages);
    const start = (page - 1) * pageSize;
    count.textContent = filtered.length ? `${start + 1}–${Math.min(start + pageSize, filtered.length)} of ${filtered.length} posts · newest first` : '0 posts';
    list.innerHTML = filtered.slice(start, start + pageSize).map(p => `<article class="post-card"><div class="post-meta"><time datetime="${escape(p.date)}">${escape(p.date)}</time><span>${escape(p.topic)}</span><span>Sample post</span></div><h2><a href="${encodeURIComponent(p.slug)}/">${escape(p.title)}</a></h2><p>${escape(p.description)}</p></article>`).join('') || '<p class="empty">No posts match your search. Try another term or reset the filters.</p>';
    pager.replaceChildren();
    function button(label, target, disabled, current = false) {
      const element = document.createElement('button');
      element.type = 'button';
      element.textContent = label;
      element.disabled = disabled;
      if (current) element.setAttribute('aria-current', 'page');
      if (/^\d+$/.test(label)) element.setAttribute('aria-label', `Page ${label}`);
      element.addEventListener('click', () => { page = target; render(); count.scrollIntoView({block:'start'}); pager.querySelector('[aria-current="page"]')?.focus({preventScroll:true}); });
      pager.append(element);
    }
    if (filtered.length > pageSize) {
      button('← Previous', page - 1, page === 1);
      for (let n = 1; n <= pages; n++) button(String(n), n, false, n === page);
      button('Next →', page + 1, page === pages);
    }
    const params = new URLSearchParams();
    if (query) params.set('q', search.value.trim());
    if (topic.value) params.set('topic', topic.value);
    if (year.value) params.set('year', year.value);
    if (page > 1) params.set('page', page);
    history.replaceState(null, '', location.pathname + (params.size ? `?${params}` : '') + location.hash);
  }
  form.addEventListener('submit', event => event.preventDefault());
  [search, topic, year].forEach(input => input.addEventListener('input', () => { page = 1; render(); }));
  form.addEventListener('reset', () => { setTimeout(() => { page = 1; render(); }, 0); });
  window.addEventListener('popstate', () => { readURL(); render(); });
  readURL();
  render();
})();
