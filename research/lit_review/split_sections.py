"""
Split arXiv papers into named section files.
Uses arXiv HTML (LaTeXML format) as primary source, falls back to pdftext heuristics.

Usage:
    python3 split_sections.py 2501.03124 2504.07831 ...
    python3 split_sections.py --all-missing   # reads missing IDs from section_split_coverage.md
"""

import sys
import os
import re
import time
import urllib.request
from pathlib import Path

SECTIONS_DIR = Path(__file__).parent / "pdfs" / "sections"
TXT_DIR = Path(__file__).parent / "pdfs" / "txt"


def fetch_html(arxiv_id: str) -> str | None:
    """Try arxiv.org/html then ar5iv fallback. Returns HTML string or None."""
    for url in [
        f"https://arxiv.org/html/{arxiv_id}",
        f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}",
    ]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            r = urllib.request.urlopen(req, timeout=15)
            content = r.read().decode("utf-8", errors="ignore")
            # ar5iv returns 200 even when unavailable, check for content
            if "No content available" in content[:2000] or len(content) < 5000:
                continue
            return content
        except Exception:
            continue
    return None


def slugify(text: str) -> str:
    """Convert section title to safe filename."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text)
    text = text[:60]
    return text or "section"


def extract_sections_html(html: str) -> list[tuple[str, str]]:
    """Extract (title, text) pairs from arXiv LaTeXML HTML."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style noise
    for tag in soup(["script", "style", "figure", "table"]):
        tag.decompose()

    sections = []

    # Extract abstract separately
    abstract_div = soup.find(class_=re.compile(r"ltx_abstract"))
    if abstract_div:
        sections.append(("abstract", abstract_div.get_text(" ", strip=True)))

    # Extract h2-level sections (main body)
    for h2 in soup.find_all("h2"):
        title = h2.get_text(" ", strip=True)
        # Collect text until next h2
        content_parts = []
        for sibling in h2.find_next_siblings():
            if sibling.name == "h2":
                break
            content_parts.append(sibling.get_text(" ", strip=True))
        content = "\n\n".join(p for p in content_parts if p)
        if title and content:
            sections.append((title, content))

    # If no h2s found, try h1 (some papers use h1 for sections)
    if len(sections) <= 1:
        for h1 in soup.find_all("h1"):
            title = h1.get_text(" ", strip=True)
            if not title or len(title) > 100:
                continue
            content_parts = []
            for sibling in h1.find_next_siblings():
                if sibling.name == "h1":
                    break
                content_parts.append(sibling.get_text(" ", strip=True))
            content = "\n\n".join(p for p in content_parts if p)
            if content:
                sections.append((title, content))

    return sections


def extract_sections_txt(arxiv_id: str) -> list[tuple[str, str]]:
    """
    Heuristic section splitting from plain text.
    Detects lines that look like section headings (short, title-like, followed by paragraphs).
    """
    txt_path = TXT_DIR / f"{arxiv_id}.txt"
    if not txt_path.exists():
        return []

    text = txt_path.read_text(errors="ignore")
    lines = text.split("\n")

    # Section heading pattern: numbered like "1 Introduction" or "2.1 Methods"
    heading_re = re.compile(
        r"^(\d+\.?\d*\.?\s+[A-Z][^\n]{3,60}|Abstract|Introduction|Conclusion[s]?|"
        r"Related Work|References|Acknowledgment[s]?|Appendix[^\n]{0,40})$"
    )

    sections = []
    current_title = "full"
    current_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if heading_re.match(stripped) and len(stripped) < 80:
            if current_lines:
                content = "\n".join(current_lines).strip()
                if content:
                    sections.append((current_title, content))
            current_title = stripped
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        content = "\n".join(current_lines).strip()
        if content:
            sections.append((current_title, content))

    # If heuristic found nothing useful, return full text as one section
    if len(sections) <= 1:
        full_text = txt_path.read_text(errors="ignore").strip()
        return [("full", full_text)]

    return sections


def write_sections(arxiv_id: str, sections: list[tuple[str, str]], source: str):
    """Write section files and index.txt."""
    out_dir = SECTIONS_DIR / arxiv_id
    out_dir.mkdir(parents=True, exist_ok=True)

    index_lines = []
    if source == "pdftext_fallback":
        index_lines.append("(pdftext fallback -- HTML not available)")

    seen_slugs: dict[str, int] = {}
    for title, content in sections:
        slug = slugify(title)
        # Deduplicate slug
        if slug in seen_slugs:
            seen_slugs[slug] += 1
            slug = f"{slug}_{seen_slugs[slug]}"
        else:
            seen_slugs[slug] = 0
        filename = f"{slug}.txt"
        (out_dir / filename).write_text(content, encoding="utf-8")
        index_lines.append(filename)

    (out_dir / "index.txt").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return len(sections)


def process_paper(arxiv_id: str) -> str:
    """Process one paper. Returns status string."""
    out_dir = SECTIONS_DIR / arxiv_id
    if out_dir.exists() and (out_dir / "index.txt").exists():
        return f"{arxiv_id}: already exists, skipping"

    # Try HTML first
    html = fetch_html(arxiv_id)
    if html:
        sections = extract_sections_html(html)
        if len(sections) >= 3:
            n = write_sections(arxiv_id, sections, "html")
            return f"{arxiv_id}: OK (HTML, {n} sections)"

    # Fall back to pdftext
    sections = extract_sections_txt(arxiv_id)
    source = "pdftext_fallback" if len(sections) <= 1 else "pdftext_heuristic"
    n = write_sections(arxiv_id, sections, source)
    return f"{arxiv_id}: fallback ({source}, {n} sections)"


def get_missing_ids() -> list[str]:
    """Read missing IDs from section_split_coverage.md."""
    coverage_path = Path(__file__).parent / "section_split_coverage.md"
    if not coverage_path.exists():
        return []
    text = coverage_path.read_text()
    # Find the "NO sections/ directory" section and extract IDs
    ids = []
    in_missing = False
    for line in text.split("\n"):
        if "NO" in line and "section" in line.lower():
            in_missing = True
            continue
        if in_missing:
            if line.startswith("#") or line.startswith("##"):
                break
            found = re.findall(r"\b(\d{4}\.\d{4,5})\b", line)
            ids.extend(found)
    return ids


if __name__ == "__main__":
    if "--all-missing" in sys.argv:
        ids = get_missing_ids()
        if not ids:
            print("No missing IDs found in section_split_coverage.md")
            sys.exit(1)
        print(f"Processing {len(ids)} missing papers: {ids}")
    else:
        ids = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not ids:
        print(__doc__)
        sys.exit(1)

    for i, arxiv_id in enumerate(ids):
        result = process_paper(arxiv_id)
        print(result)
        if i < len(ids) - 1:
            time.sleep(0.5)  # polite delay for arXiv requests
