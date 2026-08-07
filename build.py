#!/usr/bin/env python3
"""Build RedTech's canonical modular source into flat static files."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import re
import shutil

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "site-src"
DIST = ROOT / "dist"
ASSET_VERSION = "3"
PAGES = {
    "index.html": ("home.html", "RedTech | Systems, Automation & Web Consulting", "Houston-based consulting that removes repetitive work, restores failing systems, and builds useful digital tools.", "page-home", "home"),
    "solutions.html": ("solutions.html", "Fixed-Scope Solutions | RedTech", "Explore focused RedTech engagements for business automation, revenue-ready websites, and critical systems recovery.", "page-solutions", "solutions"),
    "automation-sprint.html": ("automation-sprint.html", "Business Automation Sprint | RedTech", "Replace a repetitive workflow with a documented, tested automation built around your existing systems.", "page-solution-detail", "solutions"),
    "website-sprint.html": ("website-sprint.html", "Website Revenue Sprint | RedTech", "Modernize a business website around clearer offers, stronger lead paths, accessibility, and maintainable delivery.", "page-solution-detail", "solutions"),
    "systems-rescue.html": ("systems-rescue.html", "Critical Systems Rescue | RedTech", "Diagnose and stabilize a failing system, service, deployment, or integration with a verified recovery path.", "page-solution-detail", "solutions"),
    "work.html": ("work.html", "Selected Work | RedTech", "Review anonymized examples of RedTech automation, data-layer, and systems-reliability work.", "page-work", "work"),
    "capabilities.html": ("capabilities.html", "Technical Capabilities | RedTech", "Explore RedTech capabilities across operations, security, cloud, networks, web systems, hardware, automation, and integration.", "page-capabilities", "capabilities"),
    "services.html": ("capabilities.html", "IT Services & Capabilities | RedTech", "Explore RedTech's broader technical consulting capabilities. This compatibility page provides the same catalog as Capabilities.", "page-capabilities", "capabilities"),
    "about.html": ("about.html", "About RedTech | Direct Engineering Expertise", "Meet a Houston-based consultancy with 14 years of cross-disciplinary systems, automation, support, and web experience.", "page-about", "about"),
    "contact.html": ("contact.html", "Start a Project | RedTech", "Prepare a private mailto project brief for a workflow, system, integration, website, infrastructure, or security need.", "page-contact", "contact"),
}


def read(relative: str) -> str:
    return (SRC / relative).read_text(encoding="utf-8")


def nav_state(active: str, item: str) -> str:
    return ' aria-current="page"' if active == item else ""


class ReferenceParser(HTMLParser):
    """Collect structural tags and local URL references without dependencies."""

    def __init__(self) -> None:
        super().__init__()
        self.tags = {"h1": 0, "header": 0, "footer": 0}
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.tags:
            self.tags[tag] += 1
        values = dict(attrs)
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, value))


def validate_output() -> None:
    """Fail the build for broken local references or malformed page landmarks."""
    errors: list[str] = []
    for page in PAGES:
        path = DIST / page
        document = path.read_text(encoding="utf-8")
        if re.search(r"\{\{[^{}]+\}\}", document):
            errors.append(f"{page}: unresolved placeholder")
        parser = ReferenceParser()
        parser.feed(document)
        for tag, count in parser.tags.items():
            if count != 1:
                errors.append(f"{page}: expected one <{tag}>, found {count}")
        for attribute, reference in parser.references:
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc or reference.startswith(("#", "mailto:", "tel:")):
                continue
            local_path = parsed.path
            if not local_path:
                continue
            target = (DIST / local_path).resolve()
            try:
                target.relative_to(DIST.resolve())
            except ValueError:
                errors.append(f"{page}: {attribute} escapes dist: {reference}")
                continue
            if not target.exists():
                errors.append(f"{page}: broken {attribute}: {reference}")
    if errors:
        raise RuntimeError("Build validation failed:\n- " + "\n- ".join(errors))


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    head = read("partials/head.html").replace("{{ASSET_VERSION}}", ASSET_VERSION)
    header = read("partials/header.html")
    footer = read("partials/footer.html")

    for output, meta in PAGES.items():
        source, title, description, body_class, active = meta
        nav = header
        for item in ("solutions", "work", "capabilities", "about", "contact"):
            nav = nav.replace(f"{{{{NAV_{item.upper()}}}}}", nav_state(active, item))
        document = "\n".join([
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            head,
            f"<title>{title}</title>",
            f'<meta name="description" content="{description}">',
            "</head>",
            f'<body class="{body_class}">',
            '<a class="skip-link" href="#main-content">Skip to content</a>',
            nav,
            f'<main id="main-content">\n{read(f"pages/{source}")}\n</main>',
            footer,
            f'<script src="js/interactions.js?v={ASSET_VERSION}" defer></script>',
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
    validate_output()

    for path in [DIST, *DIST.rglob("*")]:
        path.chmod(0o755 if path.is_dir() else 0o644)
    print(f"Built and validated {len(PAGES)} pages in {DIST}")


if __name__ == "__main__":
    build()
