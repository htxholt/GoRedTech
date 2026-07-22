#!/usr/bin/env python3
"""Build RedTech's modular source into flat GitHub Pages files."""

from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "site-src"
DIST = ROOT / "dist"
PAGES = {
    "index.html": {"source": "home.html", "title": "RedTech LLC | Full-Service IT Consulting", "description": "Houston-based full-service IT consulting for secure networks, cloud systems, cybersecurity, communications, websites, hardware, and ongoing support.", "body_class": "page-home", "active": "home"},
    "services.html": {"source": "services.html", "title": "IT Consulting Services | RedTech LLC", "description": "Explore RedTech's managed IT, cybersecurity, cloud, networking, communications, website, hardware, and infrastructure consulting services.", "body_class": "page-services", "active": "services"},
    "about.html": {"source": "about.html", "title": "About RedTech LLC | Practical IT Expertise", "description": "Meet RedTech, a Houston IT consultancy delivering direct engineering expertise, practical solutions, and accountable implementation.", "body_class": "page-about", "active": "about"},
    "contact.html": {"source": "contact.html", "title": "Plan an IT Project | RedTech LLC", "description": "Talk with RedTech about your IT environment, business goals, support needs, or upcoming technology project.", "body_class": "page-contact", "active": "contact"},
}


def read(relative: str) -> str:
    return (SRC / relative).read_text(encoding="utf-8")


def nav_state(active: str, item: str) -> str:
    return ' aria-current="page"' if active == item else ""


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    head = read("partials/head.html")
    header = read("partials/header.html")
    footer = read("partials/footer.html")

    for output, meta in PAGES.items():
        page = read(f"pages/{meta['source']}")
        nav = header
        for item in ("home", "services", "about", "contact"):
            nav = nav.replace(f"{{{{NAV_{item.upper()}}}}}", nav_state(meta["active"], item))
        document = "\n".join([
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            head,
            f"<title>{meta['title']}</title>",
            f'<meta name="description" content="{meta["description"]}">',
            "</head>",
            f'<body class="{meta["body_class"]}">',
            '<a class="skip-link" href="#main-content">Skip to content</a>',
            nav,
            f'<main id="main-content">\n{page}\n</main>',
            footer,
            '<script src="js/navigation.js?v=1" defer></script>',
            '<script src="js/interactions.js?v=1" defer></script>',
            "</body>",
            "</html>",
            "",
        ])
        unresolved = re.findall(r"\{\{[^{}]+\}\}", document)
        if unresolved:
            raise RuntimeError(f"Unresolved tokens in {output}: {sorted(set(unresolved))}")
        (DIST / output).write_text(document, encoding="utf-8")

    for directory in ("css", "js", "assets"):
        shutil.copytree(SRC / directory, DIST / directory)
    shutil.copy2(SRC / "CNAME", DIST / "CNAME")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    for path in DIST.rglob("*"):
        path.chmod(0o755 if path.is_dir() else 0o644)
    print(f"Built {len(PAGES)} pages in {DIST}")


if __name__ == "__main__":
    build()
