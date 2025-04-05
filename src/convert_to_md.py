import os
import docx
import re
from lxml import etree


def convert_docx_to_md(input_path: str, output_path: str):
    doc = docx.Document(input_path)
    rels = extract_hyperlinks(doc)
    md_lines = []

    for i, para in enumerate(doc.paragraphs):
        line = process_paragraph(para, rels, is_first=(i == 0))
        if line:
            md_lines.append(line)

    for table in doc.tables:
        md_lines.append(process_table(table))

    content = "\n".join(md_lines)
    content = normalize_spacing(content)

    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write(content)
    print(f"✅ Markdown saved to {output_path}")


def extract_hyperlinks(doc):
    return {r.rId: r._target for r in doc.part.rels.values() if "hyperlink" in r.reltype}


def process_paragraph(para, rels, is_first=False):
    text = extract_runs(para, rels).strip()
    if not text:
        return ""

    if is_first:
        return f"# {text}"

    if is_contact_title(text):
        return f"**{text}**"

    if is_contact_info(text):
        return text

    if is_section_header(text):
        return f"## {text}"

    if is_project_header(text):
        title, date = split_project_header(text)
        return f"### {title}\n_{date}_"

    if is_experience_title(text):
        return f"### {text}"

    if text.startswith("- ") or "•" in text:
        return f"- {text.lstrip('-• ').strip()}"

    return text


def extract_runs(para, rels):
    result = []
    root = etree.fromstring(para._element.xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    for elem in root.xpath(".//w:r | .//w:hyperlink", namespaces=ns):
        if etree.QName(elem).localname == "hyperlink":
            rel_id = elem.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            if rel_id in rels:
                url = rels[rel_id]
                text = "".join(t.text for t in elem.xpath(".//w:t", namespaces=ns))
                result.append(f"[{text}]({url})")
        else:
            t = elem.xpath(".//w:t", namespaces=ns)
            if t and t[0].text:
                text = t[0].text.strip()
                if not text:
                    continue
                is_bold = elem.xpath(".//w:b", namespaces=ns)
                is_italic = elem.xpath(".//w:i", namespaces=ns)

                if is_bold and is_italic:
                    result.append(f"***{text}***")
                elif is_bold:
                    result.append(f"**{text}**")
                elif is_italic:
                    result.append(f"*{text}*")
                else:
                    result.append(text)
    return " ".join(result)


def process_table(table):
    rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    divider = "| " + " | ".join(["---"] * len(rows[0])) + " |"
    body = "\n".join("| " + " | ".join(row) + " |" for row in rows[1:])
    return f"{header}\n{divider}\n{body}"


def normalize_spacing(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    return text.strip() + "\n"


def is_section_header(text):
    known_headers = {
        "PERFIL PROFESIONAL", "PROYECTOS DESTACADOS", "EXPERIENCIA",
        "FORMACIÓN ACADÉMICA", "HABILIDADES TÉCNICAS", "IDIOMAS"
    }
    return text.upper() in known_headers or (text.isupper() and 1 <= len(text.split()) <= 5)


def is_contact_title(text):
    return "ANALISTA DE DATOS" in text or "PROCESAMIENTO DE LENGUAJE NATURAL" in text


def is_contact_info(text):
    return (
        "@" in text or "linkedin.com" in text.lower() or "github.com" in text.lower()
        or re.search(r"\+\d{2}", text)
    )


def is_project_header(text):
    return bool(re.match(r".+\s[·\-]\s\w+", text))


def split_project_header(text):
    parts = re.split(r"\s[·\-]\s", text, maxsplit=1)
    return parts[0].strip(), parts[1].strip() if len(parts) == 2 else ("", text)


def is_experience_title(text):
    return bool(re.match(r".+[,·].+\d{4}", text))
