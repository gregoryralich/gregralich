"""Regenerate the Talkin Trash index from its post catalog (standard library only)."""
import datetime
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / 'sustainability/talkin-trash'
posts = json.loads((SERIES / 'posts.json').read_text())
posts.sort(key=lambda post: post['date'], reverse=True)
cards = []
for post in posts:
    slug = post['slug']
    if not slug or '/' in slug or slug in ('.', '..'):
        raise ValueError('Each post needs a single directory-name slug')
    if not (SERIES / slug / 'index.html').is_file():
        raise FileNotFoundError(f'Missing post page: {slug}/index.html')
    date = datetime.date.fromisoformat(post['date'])
    e = lambda value: html.escape(value, quote=True)
    cards.append(f'''<article class="post-card">
      <a class="post-image" href="{e(slug)}/" aria-label="Read {e(post['title'])}"><img src="{e(post['image'])}" alt="{e(post['image_alt'])}" width="{int(post['image_width'])}" height="{int(post['image_height'])}" decoding="async"></a>
      <div class="post-card-copy"><p class="eyebrow">{e(post['label'])}</p><h2><a href="{e(slug)}/">{e(post['title'])}</a></h2><p class="post-meta"><time datetime="{e(post['date'])}">{date.strftime('%B')} {date.day}, {date.year}</time></p><p>{e(post['summary'])}</p><a class="read-post" href="{e(slug)}/">Read the post →</a></div>
    </article>''')

document = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talkin Trash — Greg Ralich</title><meta name="description" content="An ongoing series of conversations about trash, waste, repair, reuse, and the things we choose to keep. By Greg Ralich.">
<link rel="canonical" href="https://gregralich.com/sustainability/talkin-trash/">
<meta property="og:title" content="Talkin Trash — Greg Ralich"><meta property="og:type" content="website"><meta property="og:image" content="https://gregralich.com/images/talkin-trash/low-impact-life/01-abe-fancy-lad-02.webp">
<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/sustainability/talkin-trash/talkin-trash.css"></head>
<body class="trash-page"><a class="skip-link" href="#main-content">Skip to content</a><main id="main-content">
<header class="hero trash-hero"><nav class="story-nav" aria-label="Page navigation"><a href="/sustainability.html">← Sustainability</a><a href="/index.html">Home</a><a href="#posts">The posts</a></nav><p class="eyebrow">An ongoing series by Greg Ralich</p><h1>Talkin<br>Trash</h1><p class="intro">What we use. What we keep.<br>What we throw away.</p><p class="series-description">Conversations about trash, waste, repair, and reuse—and the everyday habits behind them. It starts with five interviews I wrote for Cuppow in 2015. There’s plenty more to talk about.</p></header>
<section class="post-list" id="posts" aria-labelledby="posts-title"><div class="post-list-heading"><p class="eyebrow">The conversations</p><h2 id="posts-title">Talkin Trash posts</h2></div>
''' + '\n'.join(cards) + '''</section></main>
<footer class="site-footer"><p>Greg Ralich</p><a href="/sustainability.html">← Sustainability</a><a href="/index.html">Back home</a><a href="mailto:gregralich@gmail.com">Email me</a></footer></body></html>
'''
(SERIES / 'index.html').write_text(document)
print(f'Built Talkin Trash index: {len(posts)} post(s).')
