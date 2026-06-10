# fokhruli.github.io

Personal academic website of **Md Fokhrul Islam**, PhD Student & RA at the University of Virginia.

Live at: https://fokhruli.github.io

## Structure

```
index.html              # Home: bio, news, selected publications, latest posts
publications.html       # Full publication list (with BibTeX)
talks.html              # Talks, posters, presentations
media.html              # Press / media mentions
blog/index.html         # Blog post list
blog/posts/             # Individual blog posts (copy post-template.html)
404.html                # Custom 404 error page
assets/style.css        # All styling (light + dark themes via CSS variables)
assets/main.js          # Theme toggle, search (ctrl+k), BibTeX copy, progress bar
images/                 # Profile photo, og.jpg (social preview), icons
files/cv.pdf            # Curriculum vitae
STGCN-rehab/            # Standalone project page: GCN for rehab exercise assessment
CM-senti-analysis/      # Standalone project page: Bangla-English code-mixed sentiment analysis
sitemap.xml             # Sitemap for search engines
index.xml               # RSS feed
```

## Tech stack

Plain HTML/CSS/JS — no build step. Push to `main` and GitHub Pages deploys it.

- [Bootstrap 5.3](https://getbootstrap.com/) (nav + grid only)
- [Font Awesome 6](https://fontawesome.com/) and [Academicons](https://jpswalsh.github.io/academicons/) (icons)
- [Inter](https://fonts.google.com/specimen/Inter) (font)

Design inspired by [al-folio](https://github.com/alshedivat/al-folio).

## How to update

### Add a news item
In `index.html`, add a `news-row` at the **top** of the `news-wrap` div:
```html
<div class="news-row"><span class="news-date">Jun 2026</span><span>Something happened.</span></div>
```

### Add a publication
1. In `publications.html`, copy an existing `pub-item` block and edit the year,
   venue, title, authors, links, and BibTeX. Give the BibTeX wrapper a unique id
   (e.g. `id="bib-mypaper"`) and point the Bib button at it (`data-bib="bib-mypaper"`).
2. If it's a highlight, also update the "selected publications" section in `index.html`.
3. Add a search entry in `SEARCH_DATA` in `assets/main.js`.
4. Optionally add a news item.

### Add a blog post
1. Copy `blog/posts/post-template.html` to `blog/posts/my-post.html` and fill in
   the spots marked `CHANGE` (title, description, URLs, date, content).
2. Add a `blog-item` block at the top of the list in `blog/index.html`.
3. Update the "latest posts" list in `index.html`.
4. Add the post URL to `sitemap.xml`.

### Add a talk or media mention
Copy an existing `item-list-entry` block in `talks.html` / `media.html` and add it
at the **top** (newest first).

### Update the CV
Replace `files/cv.pdf`.

### Update the profile photo
Replace `images/fokhrul_photo.jpeg` with a **square, ~512×512, EXIF-stripped** image
(big phone photos embed GPS coordinates and slow down the page). For example:
```python
from PIL import Image
img = Image.open('new_photo.jpg').convert('RGB')   # convert() drops EXIF
img.crop(box).resize((512, 512)).save('images/fokhrul_photo.jpeg', quality=85, optimize=True)
```
Also regenerate `images/og.jpg` (1200×630) — it's the preview image shown when the
site is shared on social media.

### Yearly chore
Bump the `©` year in the footer of every HTML page:
`grep -rl "© 20" --include="*.html" .`
