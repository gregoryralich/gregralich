# gregralich.com

A deliberately simple personal website for Greg Ralich.

## The important files

### `index.html`
This is the CONTENT of the homepage.

Edit this when you want to:
- change words
- add a section
- add an image
- embed a video
- add a link
- rearrange the page

### `style.css`
This is how the site LOOKS.

Edit this when you want to change:
- colors
- type size
- spacing
- borders
- layout
- how the page behaves on phones

At the top of the CSS file are the main colors. Changing `--green` is an easy first experiment.

### `images/`
Put photos, scans, drawings, screenshots, and other images here.

For example, if you add:

`images/bike.jpg`

You can show it in `index.html` with:

`<img src="images/bike.jpg" alt="A description of the image">`

## Publishing

The root of the GitHub repository should contain `index.html` and `style.css` — don't bury them inside another folder.

Once the GitHub repo is connected to Cloudflare Pages, pushing changes to the repo will update the deployed site.

## A useful rule

Don't worry about making the code elegant yet. Make one change at a time, reload the site, and see what happened. This site is meant to become a place to learn by messing with it.
