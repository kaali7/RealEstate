from pathlib import Path
import re

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


ROOT = Path(__file__).resolve().parent.parent
DOC_DIR = ROOT / "doc"
SOURCE = DOC_DIR / "manish_doc.md"
TARGET = DOC_DIR / "manish_updated.docx"


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    field_begin = OxmlElement("w:fldChar")
    field_begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = "PAGE"
    field_end = OxmlElement("w:fldChar")
    field_end.set(qn("w:fldCharType"), "end")
    run._r.append(field_begin)
    run._r.append(instruction)
    run._r.append(field_end)


def plain(text):
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"(`+)(.*?)\1", r"\2", text)
    text = text.replace("**", "").replace("__", "")
    return text


def set_cell_text(cell, text, bold=False):
    cell.text = ""
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run(plain(text.strip()))
    run.bold = bold
    run.font.size = Pt(8.5)


def add_table(document, rows):
    if not rows:
        return
    columns = len(rows[0])
    table = document.add_table(rows=1, cols=columns)
    table.style = "Light Shading Accent 1"
    for index, value in enumerate(rows[0]):
        set_cell_text(table.rows[0].cells[index], value, bold=True)
    for row in rows[1:]:
        cells = table.add_row().cells
        for index in range(columns):
            set_cell_text(cells[index], row[index] if index < len(row) else "")
    document.add_paragraph()


def parse_table(lines, start):
    rows = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|"):
        cells = [part.strip() for part in lines[index].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            rows.append(cells)
        index += 1
    return rows, index


def add_image(document, alt, relative_path):
    image_path = DOC_DIR / relative_path.replace("/", "\\")
    if not image_path.exists():
        document.add_paragraph(f"[Image unavailable: {relative_path}]")
        return
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    run.add_picture(str(image_path), width=Inches(6.1))
    caption = document.add_paragraph(plain(alt))
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.style = "Caption"


def configure_styles(document):
    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.08

    for name, size, color in [
        ("Heading 1", 17, "123C34"),
        ("Heading 2", 14, "1F7D68"),
        ("Heading 3", 11.5, "536C66"),
    ]:
        style = document.styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(5)

    if "Code Block" not in [style.name for style in document.styles]:
        style = document.styles.add_style("Code Block", WD_STYLE_TYPE.PARAGRAPH)
    else:
        style = document.styles["Code Block"]
    style.font.name = "Consolas"
    style.font.size = Pt(8.5)
    style.paragraph_format.left_indent = Inches(0.25)
    style.paragraph_format.space_after = Pt(5)


def build():
    document = Document(str(TARGET))
    configure_styles(document)

    section = document.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)
    add_page_number(section.footer.paragraphs[0])

    document.add_page_break()

    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    in_code = False
    code_lines = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                paragraph = document.add_paragraph(style="Code Block")
                paragraph.add_run("\n".join(code_lines))
                code_lines = []
                in_code = False
            else:
                in_code = True
            index += 1
            continue
        if in_code:
            code_lines.append(line)
            index += 1
            continue

        if not stripped or stripped == "---":
            index += 1
            continue

        image_match = re.match(r"!\[([^\]]*)\]\(\./(.*)\)", stripped)
        if image_match:
            add_image(document, image_match.group(1), image_match.group(2))
            index += 1
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            document.add_heading(plain(heading.group(2)), level=len(heading.group(1)))
            index += 1
            continue

        if stripped.startswith("|"):
            rows, index = parse_table(lines, index)
            add_table(document, rows)
            continue

        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        if bullet:
            document.add_paragraph(plain(bullet.group(1)), style="List Bullet")
            index += 1
            continue

        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if numbered:
            document.add_paragraph(plain(numbered.group(1)), style="List Number")
            index += 1
            continue

        document.add_paragraph(plain(stripped))
        index += 1

    document.save(str(TARGET))


if __name__ == "__main__":
    build()
