# Talkin Trash

Series home: https://gregralich.com/sustainability/talkin-trash/

This is a static blog collection. The first post, `low-impact-life/index.html`, combines all five original 2015 Cuppow Low Impact Life interviews in full. The original interviews are sections within one post, not five blog entries. Future posts get their own directories beneath this series.

## Adding a post

1. Create `<slug>/index.html`, following the first post's document structure, shared CSS, navigation, and footer. Set its own title, description, canonical URL, date, and social image.
2. Put optimized images in `/images/talkin-trash/<slug>/`, with meaningful alt text and real width/height attributes.
3. Add an object to `posts.json` with `slug`, `title`, ISO `date`, `label`, `summary`, `image`, `image_alt`, `image_width`, and `image_height`. The slug is one directory name. Each date is that blog post's publication date, not a date of historical material inside it.
4. Run `python3 scripts/build_talkin_trash.py` from the repository root. This generates the series index, newest post first. Do not hand-edit the generated index.
5. Run `python3 scripts/check_site.py` and check the post at desktop and mobile sizes.
6. Commit the post, assets, catalog, and regenerated index together. The existing Cloudflare integration deploys the repository.

The collection needs no browser JavaScript or external CMS. It renders all post links directly in HTML. Shared styling lives in `talkin-trash.css`.

## Foundational post

- Published here November 12, 2026; interviews originally published January–May 2015.
- Complete interview text and all 24 embedded images, in original order within each interview.
- Source material: `low-impact-life-archive.zip`, preserved separately before republication.
- Image derivatives use the best explicitly exposed recovered source and are not upscaled. Camera originals were not available for all images.
- Original copy retains period-specific wording, promotions, and contact details, identified by the archive note. The new post introduction and closing are separate from those historical sections.
- A supplemental external photograph linked from Kristin's answer was unavailable; its original hyperlink remains in the interview. All embedded images are local.
