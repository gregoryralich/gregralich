(() => {
  const dialog = document.querySelector('.woodville-lightbox');
  const allLinks = [...document.querySelectorAll('a[data-gallery]')];
  if (!dialog || !allLinks.length || typeof dialog.showModal !== 'function') return;
  const title = dialog.querySelector('#gallery-title');
  const photo = dialog.querySelector('[data-gallery-image]');
  const caption = dialog.querySelector('[data-gallery-caption]');
  const count = dialog.querySelector('[data-gallery-count]');
  let current = 0;
  let links = [];
  function show(index) {
    current = (index + links.length) % links.length;
    const link = links[current];
    photo.src = link.href;
    photo.alt = link.querySelector('img').alt;
    caption.textContent = link.closest('figure').querySelector('figcaption').textContent;
    count.textContent = `${current + 1} / ${links.length}`;
  }
  allLinks.forEach(link => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    links = allLinks.filter(item => item.dataset.gallery === link.dataset.gallery);
    title.textContent = link.closest('[data-gallery-title]').dataset.galleryTitle;
    show(links.indexOf(link));
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
