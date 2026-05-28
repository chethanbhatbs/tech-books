#!/usr/bin/env python3
"""Render cover thumbnails and a feature-page image for the Python Mastery series.

Outputs:
    docs/images/python-mastery-cover.png    (page 1, ~600 px wide, dpi 160)
    docs/images/python-handbook-cover.png   (page 1, ~600 px wide, dpi 160)
    docs/images/feature-python-mastery.png  (page 9, ~1400 px wide, dpi 180)
"""
from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)


def render_cover(pdf_path: Path, out_path: Path, max_width: int = 600) -> None:
    pages = convert_from_path(str(pdf_path), dpi=160, first_page=1, last_page=1)
    img = pages[0]
    img.thumbnail((max_width, max_width * 4), Image.LANCZOS)
    img.save(out_path, "PNG", optimize=True)
    print(f"  {out_path.name}  {img.size}")


def render_feature(pdf_path: Path, page: int, out_path: Path, max_width: int = 1400) -> None:
    pages = convert_from_path(str(pdf_path), dpi=180, first_page=page, last_page=page)
    img = pages[0]
    img.thumbnail((max_width, max_width * 4), Image.LANCZOS)
    img.save(out_path, "PNG", optimize=True)
    print(f"  {out_path.name}  {img.size}  (page {page})")


if __name__ == "__main__":
    print("Covers:")
    render_cover(ROOT / "Python-Mastery.pdf", OUT / "python-mastery-cover.png")
    render_cover(ROOT / "Python-Handbook.pdf", OUT / "python-handbook-cover.png")

    print("Feature page:")
    # Page 9 of python-mastery shows the Babbage/Lovelace photographs side-by-side, the strongest
    # single-page demonstration of the book's distinctive approach.
    render_feature(ROOT / "Python-Mastery.pdf", 9, OUT / "feature-python-mastery.png")
