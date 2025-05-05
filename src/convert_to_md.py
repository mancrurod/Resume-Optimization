import os
import re
import docx
from lxml import etree

# Dictionary mapping Word styles to Markdown formatting functions
STYLE_TO_MD = {
    "Nombre": lambda text: f"# {text}",  # Map "Nombre" style to Markdown H1
    "Role": lambda text: f"**{text}**",  # Map "Role" style to bold text
    "Contacto": lambda text: f"*{text}*",  # Map "Contacto" style to italic text
    "Heading 1": lambda text: f"## {text}",  # Map "Heading 1" style to Markdown H2
    "Heading 2": lambda text: f"### {text}",  # Map "Heading 2" style to Markdown H3
    "Heading 3": lambda text: f"#### {text}",  # Map "Heading 3" style to Markdown H4
    "Bullet": lambda text: f"- {text.lstrip('-• ').strip()}",  # Map "Bullet" style to Markdown list item
    "Normal": lambda text: text,  # Map "Normal" style to plain text
}


def normalize_spacing(text: str) -> str:
    """
    Clean up excessive whitespace and newlines in the text.
    """
    text = re.sub(r"\n{3,}", "\n\n", text)  # Replace 3+ newlines with 2 newlines
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)  # Remove spaces before punctuation
    return text.strip() + "\n"  # Strip leading/trailing spaces and ensure a newline


def extract_hyperlinks(doc: docx.Document) -> dict:
    """
    Extract all hyperlinks from the Word document and map them by their relationship ID.
    """
    return {r.rId: r._target for r in doc.part.rels.values() if "hyperlink" in r.reltype}  # Map rel IDs to URLs


def extract_runs(para: docx.text.paragraph.Paragraph, rels: dict) -> str:
    """
    Extract text content from runs inside a paragraph,
    preserving formatting such as bold, italic, and hyperlinks.
    """
    result = []  # List to store formatted text
    root = etree.fromstring(para._element.xml)  # Parse paragraph XML
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}  # Define XML namespace
    seen_texts = set()  # Track already processed text to avoid duplicates

    for elem in root.xpath(".//w:hyperlink | .//w:r", namespaces=ns):  # Iterate over hyperlinks and runs
        if etree.QName(elem).localname == "hyperlink":  # If element is a hyperlink
            rel_id = elem.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")  # Get rel ID
            if rel_id in rels:  # If rel ID exists in hyperlinks
                url = rels[rel_id]  # Get URL
                text = "".join(t.text for t in elem.xpath(".//w:t", namespaces=ns) if t.text).strip()  # Extract text
                norm_text = re.sub(r"\s+", " ", text)  # Normalize whitespace
                if norm_text and norm_text not in seen_texts:  # Avoid duplicates
                    result.append(f"[{norm_text}]({url})")  # Format as Markdown link
                    seen_texts.add(norm_text)  # Mark text as seen
        elif etree.QName(elem).localname == "r":  # If element is a run
            if elem.getparent() is not None and etree.QName(elem.getparent()).localname == "hyperlink":
                continue  # Skip runs inside hyperlinks
            t = elem.xpath(".//w:t", namespaces=ns)  # Extract text nodes
            if t and t[0].text:  # If text exists
                text = t[0].text.strip()  # Get text content
                norm_text = re.sub(r"\s+", " ", text)  # Normalize whitespace
                if not norm_text or norm_text in seen_texts:  # Skip empty or duplicate text
                    continue

                # Detect formatting
                is_bold = elem.xpath(".//w:b", namespaces=ns)  # Check for bold formatting
                is_italic = elem.xpath(".//w:i", namespaces=ns)  # Check for italic formatting

                if is_bold and is_italic:  # If both bold and italic
                    result.append(f"***{norm_text}***")  # Format as bold+italic
                elif is_bold:  # If bold only
                    result.append(f"**{norm_text}**")  # Format as bold
                elif is_italic:  # If italic only
                    result.append(f"*{norm_text}*")  # Format as italic
                else:  # If no formatting
                    result.append(norm_text)  # Add plain text

                seen_texts.add(norm_text)  # Mark text as seen

    return " ".join(result)  # Join all formatted text


def process_paragraph(para: docx.text.paragraph.Paragraph, rels: dict) -> str:
    """
    Convert a single paragraph into Markdown format based on its Word style.
    """
    text = extract_runs(para, rels).strip()  # Extract and format paragraph text
    if not text:  # Skip empty paragraphs
        return ""

    style = para.style.name  # Get paragraph style

    # Use predefined style mappings
    if style in STYLE_TO_MD:
        return STYLE_TO_MD[style](text)  # Apply Markdown formatting based on style

    # Handle bullet-like lines without explicit style
    if text.startswith("- ") or "•" in text:
        return f"- {text.lstrip('-• ').strip()}"  # Format as Markdown list item

    return text  # Return plain text if no specific style matches


def process_table(table: docx.table.Table) -> str:
    """
    Convert a Word table into a Markdown-style table (basic implementation).
    """
    rows = []  # List to store table rows
    for row in table.rows:  # Iterate over table rows
        cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]  # Extract and clean cell text
        rows.append("| " + " | ".join(cells) + " |")  # Format row as Markdown table row

    if len(rows) >= 2:  # If table has at least two rows
        header_sep = "| " + " | ".join("---" for _ in rows[0].split("|") if _ and _ != " ") + " |"  # Create header separator
        return "\n".join([rows[0], header_sep] + rows[1:])  # Combine header, separator, and rows
    return "\n".join(rows)  # Return rows if no header


def convert_docx_to_md(input_path: str, output_path: str) -> None:
    """
    Convert a .docx resume file into a structured Markdown (.md) file.
    
    This function parses paragraphs and tables from a Word document,
    applies Markdown formatting based on paragraph styles, and inserts
    blank lines when transitioning between list items and new sections 
    (e.g., new work or education entries) to preserve the visual structure
    of the original document.
    
    Parameters:
    ----------
    input_path : str
        Path to the input .docx file.
    output_path : str
        Path where the output .md file will be saved.
    """
    doc = docx.Document(input_path)  # Load the Word document
    rels = extract_hyperlinks(doc)  # Extract hyperlink relationships
    md_lines = []  # List to store Markdown lines

    previous_style = ""  # Track the style of the previous paragraph

    for para in doc.paragraphs:  # Process each paragraph in the document
        line = process_paragraph(para, rels)  # Convert paragraph to Markdown
        if not line:  # Skip empty lines
            continue

        current_style = para.style.name  # Get current paragraph style

        # Insert a blank line when transitioning from a bullet list or normal text
        # to a new heading or different paragraph style
        if (
            previous_style in ("Bullet", "Normal")
            and current_style not in ("Bullet", "Normal")
        ):
            md_lines.append("")  # Insert blank line for readability

        md_lines.append(line)  # Add the formatted line to the Markdown output
        previous_style = current_style  # Update previous style

    for table in doc.tables:  # Process and append any tables in the document
        md_lines.append(process_table(table))  # Convert table to Markdown

    content = "\n".join(md_lines)  # Combine all lines into a single Markdown string
    content = normalize_spacing(content)  # Normalize spacing in the content

    with open(output_path, "w", encoding="utf-8") as md_file:  # Save the final Markdown output to file
        md_file.write(content)  # Write content to file

    print(f"✅ Markdown saved to {output_path}")  # Print success message
