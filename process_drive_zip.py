#!/usr/bin/env python3
"""Unzip a Drive ZIP, auto-crop black borders, deduplicate, classify files, and organize outputs.

Usage:
  python3 process_drive_zip.py /path/to/drive-download-...zip

Dependencies:
  pip install Pillow pymupdf python-docx

The script creates an `organized/` directory next to the ZIP with subfolders
like `certificates/`, `publications/`, `internships/`, `awards/`, and `others/`.
"""
from __future__ import annotations

import sys
import os
import zipfile
import shutil
import hashlib
from pathlib import Path
from io import BytesIO

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

try:
    from docx import Document
except Exception:
    Document = None

from PIL import Image


def unzip_to(zip_path: Path, dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(dest)


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def autocrop_black(img: Image.Image, threshold: int = 10) -> Image.Image:
    gray = img.convert('L')
    bw = gray.point(lambda p: 255 if p > threshold else 0, '1')
    bbox = bw.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def classify_text(text: str) -> str:
    txt = (text or '').lower()
    if any(k in txt for k in ['certificate', 'certified', 'certificate of']):
        return 'certificates'
    if any(k in txt for k in ['publication', 'paper', 'journal', 'proceeding']):
        return 'publications'
    if any(k in txt for k in ['intern', 'internship']):
        return 'internships'
    if any(k in txt for k in ['award', 'achievement', 'winner']):
        return 'awards'
    return 'others'


def classify_by_name(name: str) -> str | None:
    n = name.lower()
    if any(k in n for k in ['cert', 'certificate']):
        return 'certificates'
    if any(k in n for k in ['pub', 'publication', 'paper']):
        return 'publications'
    if any(k in n for k in ['intern']):
        return 'internships'
    if any(k in n for k in ['award']):
        return 'awards'
    return None


def save_image(img: Image.Image, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)


def process_image(path: Path, out_base: Path, seen_hashes: set[str]):
    try:
        h = file_hash(path)
        if h in seen_hashes:
            return
        seen_hashes.add(h)
        img = Image.open(path)
    except Exception as e:
        print('Failed to open image', path, e)
        return
    category = classify_by_name(path.name) or 'others'
    cropped = autocrop_black(img)
    out_dir = out_base / category / 'images'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / path.name
    save_image(cropped, out_file)


def process_pdf(path: Path, out_base: Path, seen_hashes: set[str]):
    h = file_hash(path)
    if h in seen_hashes:
        return
    seen_hashes.add(h)
    text = ''
    if fitz is not None:
        try:
            doc = fitz.open(str(path))
            for page in doc:
                try:
                    text += page.get_text() or ''
                except Exception:
                    pass
        except Exception as e:
            print('Failed to read PDF', path, e)
    category = classify_text(text) or classify_by_name(path.name) or 'others'
    # copy pdf
    pdf_out_dir = out_base / category / 'pdfs'
    pdf_out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, pdf_out_dir / path.name)
    # render pages to images if possible
    if fitz is None:
        return
    try:
        doc = fitz.open(str(path))
        images_out_dir = out_base / category / 'images'
        images_out_dir.mkdir(parents=True, exist_ok=True)
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=200)
            img_data = pix.tobytes('png')
            img = Image.open(BytesIO(img_data))
            cropped = autocrop_black(img)
            save_image(cropped, images_out_dir / f"{path.stem}_page{i}.png")
    except Exception as e:
        print('Failed to render PDF pages', path, e)


def process_docx(path: Path, out_base: Path, seen_hashes: set[str]):
    h = file_hash(path)
    if h in seen_hashes:
        return
    seen_hashes.add(h)
    text = ''
    if Document is not None:
        try:
            doc = Document(path)
            for p in doc.paragraphs:
                text += p.text + '\n'
        except Exception as e:
            print('Failed to parse docx', path, e)
    category = classify_text(text) or classify_by_name(path.name) or 'others'
    target = out_base / category / 'docs'
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target / path.name)


def main(zip_path_str: str):
    zip_path = Path(zip_path_str)
    if not zip_path.exists():
        print('ZIP not found:', zip_path)
        return
    work_dir = zip_path.parent
    unzip_dir = work_dir / (zip_path.stem + '_unzipped')
    print('Unzipping to', unzip_dir)
    unzip_to(zip_path, unzip_dir)
    out_base = work_dir / 'organized'
    out_base.mkdir(parents=True, exist_ok=True)
    seen_hashes: set[str] = set()
    for root, dirs, files in os.walk(unzip_dir):
        for f in files:
            p = Path(root) / f
            suf = p.suffix.lower()
            try:
                if suf in ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp', '.gif']:
                    print('Image:', p.name)
                    process_image(p, out_base, seen_hashes)
                elif suf == '.pdf':
                    print('PDF:', p.name)
                    process_pdf(p, out_base, seen_hashes)
                elif suf in ['.docx']:
                    print('DOCX:', p.name)
                    process_docx(p, out_base, seen_hashes)
                else:
                    # copy other files into others/raw, deduping
                    h = file_hash(p)
                    if h in seen_hashes:
                        continue
                    seen_hashes.add(h)
                    target = out_base / 'others' / 'raw'
                    target.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, target / p.name)
            except Exception as e:
                print('Error processing', p, e)

    print('Done. Organized files under', out_base)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 process_drive_zip.py /path/to/archive.zip')
        sys.exit(1)
    main(sys.argv[1])
