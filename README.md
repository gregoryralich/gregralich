# gregralich.com

A static personal website. HTML and CSS are served directly; there is no build step, database, application server, or JavaScript package dependency.

## Editing

- `index.html`: homepage content.
- `bicycles.html` and `bicycles.css`: bicycle portfolio and page-specific layout.
- `jims-photos.html`, `amesbury-postcards.html`, and `welcome-to-looserville.html`: photo stories, sharing `story.css`.
- `cross-country.html` through `cross-country-5.html`: original trip journal, sharing `cross-country.css`.
- `style.css`: shared colors, typography, layout, navigation, footers, and press cards. Change the variables at the top for site-wide colors and widths.
- `images/`: images and existing archive media used by the site. Keep paths and letter case exact.

Use `<p>` for a paragraph, a list for a group of entries, and CSS for spacing. Keep layout rules in the stylesheets. When adding an image, provide meaningful alternative text and use a web-sized copy while preserving the original elsewhere.

## Preview and checks

From the repository root:

```sh
python3 -m http.server 8000
```

Open http://localhost:8000. To validate the site:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/check_site.py
```

GitHub Actions runs the same check on pushes and pull requests. It checks HTML parsing, local file references, fragment links, duplicate IDs, and archive exclusions. It does not check whether external websites are available. Validation dependencies are development-only and are not shipped to visitors.

## Deployment and security

Cloudflare serves static files from the repository root. `.assetsignore` excludes repository metadata, documentation, validation scripts, and `archive/` from Workers static-asset uploads. `.gitignore` prevents local Mac metadata and environment files from entering Git; it does not control deployment.

The archive exclusion depends on the Workers static-assets uploader honoring `.assetsignore`. If switching to Cloudflare Pages or another host, deploy an explicit public-only directory rather than uploading the whole repository. Never publish `archive/`.

`_headers` sets MIME-sniffing protection, prevents other sites framing this site, limits referrer information, and disables unneeded device permissions. Its Content Security Policy blocks object embeds, base-URL changes to other origins, framing, and form submissions. It does not yet restrict all script and network origins: YouTube, Instagram, and Ride with GPS require browser testing before a stricter policy is enabled. Verify these headers on the deployed domain after publication.

`404.html` is the not-found page. Keep static hosting configured to return a real 404 for missing paths rather than falling back to the homepage.

## Preserved audio

The four original Tumblr MP3 files are preserved byte-for-byte in `archive/audio/`. They are not linked by public pages and are excluded from asset uploads. A public repository still makes these files accessible through GitHub. The website's existing “Audio omitted from this archive” notes remain accurate.

Image optimization and archival image descriptions are separate follow-up work. No original image files were changed during the source cleanup.
