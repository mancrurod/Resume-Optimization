import os
import docx
import re
from lxml import etree

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

def normalize_spacing(text):
    import re
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    return text.strip() + "\n"


def convert_docx_to_md(input_path: str, output_path: str):
    doc = docx.Document(input_path)
    rels = extract_hyperlinks(doc)
    md_lines = []

    for para in doc.paragraphs:
        line = process_paragraph(para, rels)
        if line:
            md_lines.append(line)

    for table in doc.tables:
        md_lines.append(process_table(table))

    content = "\n".join(md_lines)
    content = normalize_spacing(content)

    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(content)
    print(f"\u2705 Markdown saved to {output_path}")

def extract_hyperlinks(doc):
    return {r.rId: r._target for r in doc.part.rels.values() if "hyperlink" in r.reltype}

def process_paragraph(para, rels):
    text = extract_runs(para, rels).strip()
    if not text:
        return ""

    style = para.style.name
    if style in STYLE_TO_MD:
        return STYLE_TO_MD[style](text)
    if text.startswith("- ") or "•" in text:
        return f"- {text.lstrip('-• ').strip()}"
    return text

def extract_runs(para, rels):
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
            # Solo procesamos si este <w:r> no está dentro de un <w:hyperlink>
            if elem.getparent() is not None and etree.QName(elem.getparent()).localname == "hyperlink":
                continue
            t = elem.xpath(".//w:t", namespaces=ns)
            if t and t[0].text:
                text = t[0].text.strip()
                norm_text = re.sub(r"\s+", " ", text)
                if not norm_text or norm_text in seen_texts:
                    continue
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
