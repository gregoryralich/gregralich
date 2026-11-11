(() => {
  const dialog = document.querySelector('.woodville-lightbox');
  const links = [...document.querySelectorAll('[data-gallery="tim"]')];
  if (!dialog || !links.length || typeof dialog.showModal !== 'function') return;
  const photo = dialog.querySelector('[data-gallery-image]');
  const caption = dialog.querySelector('[data-gallery-caption]');
  const count = dialog.querySelector('[data-gallery-count]');
  let current = 0;
  function show(index) {
    current = (index + links.length) % links.length;
    const link = links[current];
    photo.src = link.href;
    photo.alt = link.querySelector('img').alt;
    caption.textContent = link.closest('figure').querySelector('figcaption').textContent;
    count.textContent = `${current + 1} / ${links.length}`;
  }
  links.forEach((link, index) => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    show(index);
    dialog.showModal();
  }));
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-previous]').addEventListener('click', () => show(current - 1));
  dialog.querySelector('[data-next]').addEventListener('click', () => show(current + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      show(current + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });
})();
