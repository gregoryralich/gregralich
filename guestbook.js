(() => {
  'use strict';
  const API = 'https://greg-ralich-guestbook.sincerecob2.chatgpt.site';
  async function request(path, options) {
    const response = await fetch(API + path, options);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Please try again in a moment.');
    return data;
  }
  const counter = document.querySelector('[data-visit-counter]');
  if (counter) {
    request('/api/visits', { method: 'POST' }).then(({ count }) => {
      const value = String(count).padStart(7, '0');
      counter.replaceChildren(...[...value].map(digit => {
        const cell = document.createElement('span'); cell.textContent = digit; cell.setAttribute('aria-hidden', 'true'); return cell;
      }));
      counter.setAttribute('aria-label', count.toLocaleString() + ' visits since November 2026');
    }).catch(() => {
      counter.setAttribute('aria-label', 'Visit counter temporarily unavailable');
      const note = document.querySelector('[data-counter-note]');
      if (note) note.textContent = 'Counter taking a breather. Come back soon.';
    });
  }
  const form = document.querySelector('.guestbook-form');
  if (!form) return;
  const button = form.querySelector('button[type="submit"]');
  const status = document.querySelector('#form-status');
  let token = '';
  async function refreshToken() {
    button.disabled = true;
    try { token = (await request('/api/form-token')).token; button.disabled = false; }
    catch { status.textContent = 'The guestbook could not connect. Please refresh to try again.'; }
  }
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity() || button.disabled) return;
    button.disabled = true; status.textContent = 'Sending your note…';
    const values = Object.fromEntries(new FormData(form));
    try {
      await request('/api/entries', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({...values,token}) });
      form.reset(); status.textContent = 'Thanks for stopping by! Your note is waiting for Greg’s approval.';
    } catch (error) { status.textContent = error.message; }
    await refreshToken();
  });
  refreshToken();
  let cursor = '', loading = false;
  const entries = document.querySelector('#guestbook-entries');
  const entriesStatus = document.querySelector('#entries-status');
  const more = document.querySelector('#guestbook-more');
  function render(entry) {
    const article = document.createElement('article'); article.className = 'guestbook-entry';
    const name = document.createElement('h3'); name.textContent = entry.name;
    const date = document.createElement('time'); date.dateTime = new Date(entry.createdAt).toISOString();
    date.textContent = new Date(entry.createdAt).toLocaleDateString(undefined, {year:'numeric',month:'long',day:'numeric'});
    const message = document.createElement('p'); message.textContent = entry.message;
    article.append(name, date, message);
    if (entry.website) {
      const url = new URL(entry.website);
      if (url.protocol === 'https:' || url.protocol === 'http:') {
        const link = document.createElement('a'); link.href = url.href; link.textContent = 'Visit ' + url.hostname + ' ↗';
        link.rel = 'nofollow ugc noopener noreferrer'; link.target = '_blank'; article.append(link);
      }
    }
    entries.append(article);
  }
  async function loadEntries() {
    if (loading) return; loading = true; more.disabled = true; entriesStatus.textContent = 'Opening the guestbook…';
    try {
      const data = await request('/api/entries' + (cursor ? '?before=' + encodeURIComponent(cursor) : ''));
      data.entries.forEach(render); cursor = data.next || ''; more.hidden = !cursor;
      entriesStatus.textContent = entries.children.length ? '' : 'The pages are fresh. Be the first to leave a note.';
    } catch { entriesStatus.textContent = 'Could not load the guestbook. Refresh to try again.'; }
    finally { loading = false; more.disabled = false; }
  }
  more.addEventListener('click', loadEntries); loadEntries();
})();
