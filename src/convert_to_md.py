import os
import docx
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from lxml import etree  # Import lxml for XML parsing

def convert_docx_to_md(input_path: str, output_path: str):
    """Converts a .docx file to Markdown format while preserving formatting."""
    doc = docx.Document(input_path)
    md_lines = []
    rels = extract_hyperlinks(doc)
    
    for para in doc.paragraphs:
        process_paragraph(para, md_lines, rels)
    
    for table in doc.tables:
        process_table(table, md_lines)
    
    with open(output_path, "w", encoding="utf-8") as md_file:
        md_file.write("\n".join(md_lines))
    print(f"✅ Markdown file saved: {output_path}")

def extract_hyperlinks(doc):
    """Extracts hyperlinks from the document relationships."""
    hyperlinks = {}
    for rel in doc.part.rels.values():
        if "hyperlink" in rel.reltype:
            hyperlinks[rel.rId] = rel._target
    return hyperlinks

def process_paragraph(para, md_lines, rels):
    """Processes a paragraph and converts it to Markdown."""
    text = process_runs(para, rels)
    if not text.strip():
        md_lines.append("")
        return
    
    style_name = para.style.name.lower() if para.style else ""
    if "heading" in style_name:
        heading_level = min(extract_heading_level(style_name), 6)
        md_lines.append(f"{'#' * heading_level} {text}")
    elif is_bulleted_list(para):
        md_lines.append(f"- {text}")  # Treat as bullet point in Markdown
    elif is_numbered_list(para):
        md_lines.append(f"1. {text}")
    elif para.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
        md_lines.append(f"<div align=\"center\">{text}</div>")
    else:
        md_lines.append(text)

def process_runs(para, rels):
    """Processes runs to apply Markdown styling and retain hyperlinks."""
    result = []
    para_xml = para._element.xml  # Get the XML of the paragraph
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    
    # Parse the XML using lxml
    root = etree.fromstring(para_xml)
    
    # Iterate through all elements in the paragraph
    for elem in root.xpath(".//w:r | .//w:hyperlink", namespaces=ns):
        if etree.QName(elem).localname == "hyperlink":
            # Handle hyperlink
            rel_id = elem.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            if rel_id in rels:
                # Extract text from child runs
                hyperlink_text = "".join(run.text for run in elem.xpath(".//w:r/w:t", namespaces=ns))
                hyperlink_url = rels[rel_id]
                result.append(f"[{hyperlink_text}]({hyperlink_url})")
        else:
            # Handle regular run
            text_elem = elem.xpath(".//w:t", namespaces=ns)
            if text_elem:
                text = text_elem[0].text.strip()
                if text:
                    # Skip if this text is already part of a hyperlink
                    if result and result[-1].endswith(")") :
                        continue
                    # Apply text styles (bold, italic)
                    is_bold = elem.xpath(".//w:b", namespaces=ns) != []
                    is_italic = elem.xpath(".//w:i", namespaces=ns) != []
                    if is_bold and is_italic:
                        result.append(f"***{text}***")
                    elif is_bold:
                        result.append(f"**{text}**")
                    elif is_italic:
                        result.append(f"*{text}*")
                    else:
                        result.append(text)
    return " ".join(result)  # Join with spaces to avoid concatenation issues

def apply_text_styles(run, text):
    """Applies Markdown styles for bold and italics."""
    if run.bold and run.italic:
        return f"***{text}***"
    elif run.bold:
        return f"**{text}**"
    elif run.italic:
        return f"*{text}*"
    return text

def is_bulleted_list(para):
    """Detects if a paragraph is a bulleted list item."""
    if para.style and para.style.name:
        # Check if the style name is a type of bullet list
        return "bullet" in para.style.name.lower() or "list" in para.style.name.lower()
    return False

def is_numbered_list(para):
    """Detects if a paragraph is a numbered list item."""
    if para.style and para.style.name:
        # Check if the style name indicates a numbered list
        return "number" in para.style.name.lower() or "list" in para.style.name.lower()
    return False

def extract_heading_level(style_name):
    """Extracts heading level from style name."""
    for i in range(1, 7):
        if f"heading {i}" in style_name:
            return i
    return 1

def process_table(table, md_lines):
    """Converts a table to Markdown format."""
    rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]
    if not rows:
        return
    
    md_lines.append("| " + " | ".join(rows[0]) + " |")
    md_lines.append("| " + " | ".join(["---"] * len(rows[0])) + " |")
    for row in rows[1:]:
        md_lines.append("| " + " | ".join(row) + " |")
    md_lines.append("")

if __name__ == "__main__":
    input_file = "Manuel Cruz Rodríguez CV.docx"
    output_file = "Manuel_Cruz_Rodriguez_CV.md"
    convert_docx_to_md(input_file, output_file)
