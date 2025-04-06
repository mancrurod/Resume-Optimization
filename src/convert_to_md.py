import os
import re
import docx
from lxml import etree

# Dictionary mapping Word styles to Markdown formatting functions
STYLE_TO_MD = {
    "Nombre": lambda text: f"# {text}",
    "Role": lambda text: f"**{text}**",
    "Contacto": lambda text: f"*{text}*",
    "Heading 1": lambda text: f"## {text}",
    "Heading 2": lambda text: f"### {text}",
    "Heading 3": lambda text: f"#### {text}",
    "Bullet": lambda text: f"- {text.lstrip('-• ').strip()}",
    "Normal": lambda text: text,
}


def normalize_spacing(text: str) -> str:
    """
    Clean up excessive whitespace and newlines in the text.
    """
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    return text.strip() + "\n"


def extract_hyperlinks(doc: docx.Document) -> dict:
    """
    Extract all hyperlinks from the Word document and map them by their relationship ID.
    """
    return {r.rId: r._target for r in doc.part.rels.values() if "hyperlink" in r.reltype}


def extract_runs(para: docx.text.paragraph.Paragraph, rels: dict) -> str:
    """
    Extract text content from runs inside a paragraph,
    preserving formatting such as bold, italic, and hyperlinks.
    """
    result = []
    root = etree.fromstring(para._element.xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    seen_texts = set()

    for elem in root.xpath(".//w:hyperlink | .//w:r", namespaces=ns):
        if etree.QName(elem).localname == "hyperlink":
            rel_id = elem.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            if rel_id in rels:
                url = rels[rel_id]
                text = "".join(t.text for t in elem.xpath(".//w:t", namespaces=ns) if t.text).strip()
                norm_text = re.sub(r"\s+", " ", text)
                if norm_text and norm_text not in seen_texts:
                    result.append(f"[{norm_text}]({url})")
                    seen_texts.add(norm_text)
        elif etree.QName(elem).localname == "r":
            # Skip if run is inside a hyperlink
            if elem.getparent() is not None and etree.QName(elem.getparent()).localname == "hyperlink":
                continue
            t = elem.xpath(".//w:t", namespaces=ns)
            if t and t[0].text:
                text = t[0].text.strip()
                norm_text = re.sub(r"\s+", " ", text)
                if not norm_text or norm_text in seen_texts:
                    continue

                # Detect formatting
                is_bold = elem.xpath(".//w:b", namespaces=ns)
                is_italic = elem.xpath(".//w:i", namespaces=ns)

                if is_bold and is_italic:
                    result.append(f"***{norm_text}***")
                elif is_bold:
                    result.append(f"**{norm_text}**")
                elif is_italic:
                    result.append(f"*{norm_text}*")
                else:
                    result.append(norm_text)

                seen_texts.add(norm_text)

    return " ".join(result)


def process_paragraph(para: docx.text.paragraph.Paragraph, rels: dict) -> str:
    """
    Convert a single paragraph into Markdown format based on its Word style.
    """
    text = extract_runs(para, rels).strip()
    if not text:
        return ""

    style = para.style.name

    # Use predefined style mappings
    if style in STYLE_TO_MD:
        return STYLE_TO_MD[style](text)

    # Handle bullet-like lines without explicit style
    if text.startswith("- ") or "•" in text:
        return f"- {text.lstrip('-• ').strip()}"

    return text


def process_table(table: docx.table.Table) -> str:
    """
    Convert a Word table into a Markdown-style table (basic implementation).
    """
    rows = []
    for row in table.rows:
        cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
        rows.append("| " + " | ".join(cells) + " |")

    if len(rows) >= 2:
        header_sep = "| " + " | ".join("---" for _ in rows[0].split("|") if _ and _ != " ") + " |"
        return "\n".join([rows[0], header_sep] + rows[1:])
    return "\n".join(rows)


def convert_docx_to_md(input_path: str, output_path: str) -> None:
    """
    Main function that converts a .docx file into a Markdown (.md) file.
    """
    doc = docx.Document(input_path)
    rels = extract_hyperlinks(doc)
    md_lines = []

    # Process paragraphs
    for para in doc.paragraphs:
        line = process_paragraph(para, rels)
        if line:
            md_lines.append(line)

    # Process tables
    for table in doc.tables:
        md_lines.append(process_table(table))

    # Combine and clean text
    content = "\n".join(md_lines)
    content = normalize_spacing(content)

    # Write Markdown output
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(content)

    print(f"\u2705 Markdown saved to {output_path}")
