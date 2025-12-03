# generate_gallery.py

from pathlib import Path
from PIL import Image            # make sure Pillow is installed:  pip3 install Pillow
import re


# ---------- CONFIG YOU CHANGE PER GALLERY ----------

SLUG = "turpinbasketball"          # folder name under images/ AND html filename (no .html)
PAGE_TITLE = "Turpin Basketball – Parker Jones"

GALLERY_FOLDER = Path(f"images/sports/turpinbasketball")
OUTPUT_HTML = Path(f"turpinbasketball.html")


# ---------- HELPERS ----------

def is_landscape(image_path: Path) -> bool:
    """Return True if image is wider than tall."""
    with Image.open(image_path) as img:
        width, height = img.size
    return width > height


def build_page(gallery_html: str) -> str:
    """Wrap the gallery HTML in your full page boilerplate."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{PAGE_TITLE}</title>
    <link rel="stylesheet" href="styles.css" />
    <link rel="icon" type="image/png" href="logo.png" />
    <meta name="mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="default" />
</head>
<body>
<div class="content">

    <!-- HEADER -->
    <div class="header">
        <!-- left: name -->
        <ul class="left-links">
            <li><a href="#">Parker Jones</a></li>
        </ul>

        <!-- hamburger button (only shows on small screens) -->
        <button class="menu-toggle" aria-label="Toggle navigation">
            <span class="bar"></span>
            <span class="bar"></span>
        </button>

        <!-- right: normal nav links -->
        <ul class="right-links">
            <li><a href="index.html" class="nav-link">Home</a></li>
            <li><a href="photography.html" class="nav-link">Photography</a></li>
            <li><a href="about.html" class="nav-link">About</a></li>
            <li><a href="contact.html" class="nav-link">Contact</a></li>
        </ul>
    </div>

    <!-- MAIN PHOTOGRAPHY PAGE -->
    <main class="photography-page">
{gallery_html}
    </main>

    <!-- FOOTER -->
    <footer class="site-footer">
        <div class="footer-left">
            Parker G Jones
        </div>
        <div class="footer-right">
            <a href="https://instagram.com/Life_ofpjones" target="_blank" class="instagram-link" rel="noopener">
                <img src="instagram.webp" alt="Instagram" class="instagram-icon" />
            </a>
        </div>
    </footer>

</div><!-- /.content -->

<!-- LIGHTBOX OVERLAY -->
<div class="lightbox" id="lightbox">
    <div class="lightbox-backdrop"></div>
    <div class="lightbox-content">
        <button class="lightbox-close" aria-label="Close image">&times;</button>
        <img id="lightbox-image" src="" alt="Large view" />
    </div>
</div>

<script src="js/lightbox.js"></script>
<script>
    const header = document.querySelector('.header');
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelectorAll('.right-links a');

    menuToggle.addEventListener('click', () => {{
        header.classList.toggle('open');
    }});

    // optional: close menu when a link is clicked
    navLinks.forEach(link => {{
        link.addEventListener('click', () => {{
            header.classList.remove('open');
        }});
    }});
</script>

</body>
</html>
"""


# ---------- MAIN SCRIPT ----------

def main():
    # 1. Collect all jpg/png/webp files in that folder
    files = [
        f
        for f in GALLERY_FOLDER.iterdir()
        if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
    ]

    if not files:
        print(f"No images found in {GALLERY_FOLDER}")
        return

    # 2. Sort files by numeric order inside the filename (IMG_2573 < IMG_2608)
    def extract_number(path: Path) -> int:
        match = re.search(r"(\d+)", path.name)
        return int(match.group(1)) if match else 0

    files.sort(key=extract_number)

    # 3. Build just the gallery section HTML (your 6-slot grid; CSS handles layout)
    figure_lines = []
    for idx, img_path in enumerate(files, start=1):
        rel_path = img_path.as_posix()   # path like images/astonmartinDBS/IMG_xxx.jpg
        alt_text = f"Photo {idx}"

        if is_landscape(img_path):
            cls = "photo-item photo-wide"   # landscape = takes 2 columns via CSS
        else:
            cls = "photo-item"

        figure_lines.append(
            f'        <figure class="{cls}">\n'
            f'            <img src="{rel_path}" alt="{alt_text}" />\n'
            f'        </figure>'
        )

    gallery_html = (
        '        <section class="photo-section">\n'
        '            <div class="photo-grid">\n'
        + "\n".join(figure_lines)
        + "\n            </div>\n"
        "        </section>\n"
    )

    # 4. Wrap in full page boilerplate
    full_page = build_page(gallery_html)

    # 5. Write the HTML file
    OUTPUT_HTML.write_text(full_page, encoding="utf-8")
    print(f"Wrote {OUTPUT_HTML} with {len(files)} images.")


if __name__ == "__main__":
    main()
