import sys
import os
import markdown2
import pdfkit
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, 
    QHBoxLayout, QLineEdit, QDialog, QFormLayout, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


# ---------- UTILS ----------
def remove_code_block_wrapper(md_text: str) -> str:
    lines = md_text.strip().splitlines()
    if lines and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return "\n".join(lines[1:-1]).strip()
    return md_text

def normalize_markdown(md_text: str) -> str:
    lines = md_text.splitlines()
    return "\n".join(line.strip() for line in lines)


# ---------- MARKDOWN TO HTML ----------
def convert_md_to_html(md_path, html_path):
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    with open(md_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    md_content = remove_code_block_wrapper(md_content)
    md_content = normalize_markdown(md_content)

    lines = md_content.strip().splitlines()
    name = ""
    role = ""
    contact_lines = []
    content_lines = []
    i = 0

    if lines and lines[0].startswith("# "):
        name = lines[0][2:].strip()
        i += 1

    if i < len(lines) and lines[i].startswith("**") and lines[i].endswith("**"):
        role = lines[i].strip("*").strip()
        i += 1

    while i < len(lines) and lines[i].strip() and not lines[i].startswith("##"):
        contact_lines.append(lines[i].strip())
        i += 1

    content_lines = lines[i:]
    html_body = markdown2.markdown("\n".join(content_lines), extras=[
        "fenced-code-blocks", "tables", "strike", "cuddled-lists", "metadata", "footnotes"
    ])

    header_html = ""
    if name:
        header_html += f"<h1>{name}</h1>\n"
    if role:
        header_html += f"<p><strong>{role}</strong></p>\n"
    for line in contact_lines:
        if re.match(r"^_?.*\d{4}.*_?$", line):  # si parece una fecha
            header_html += f'<p class="date">{line.strip("_")}</p>\n'
        else:
            header_html += markdown2.markdown(line)

    html_document = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resume</title>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@600&family=Roboto:wght@400&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Roboto', sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            margin: 2em auto;
            max-width: 800px;
            color: #222;
        }}
        h1, h2 {{
            font-family: 'EB Garamond', serif;
            font-weight: 600;
            color: #222;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
        }}
        h3, h4 {{
            font-family: 'Roboto', sans-serif;
            font-size: 11pt;
            font-weight: 600;
            color: #222;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
        }}
        .date {{
            font-size: 10pt;
            font-style: italic;
            margin-bottom: 0.5em;
        }}
        p {{
            margin-bottom: 0.8em;
        }}
        ul, ol {{
            padding-left: 2em;
            margin-bottom: 1em;
        }}
        ul li, ol li {{
            margin-bottom: 4px;
        }}
        #idiomas li {{
            list-style-type: "– ";
            margin-left: 1em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }}
        a {{
            color: #0056b3;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body contenteditable="true">
{header_html}
{html_body}
</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_document)


# ---------- HTML TO PDF ----------
def convert_html_to_pdf(html_path, pdf_path):
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    options = {
        'encoding': 'UTF-8', 'page-size': 'A4', 'margin-top': '20mm',
        'margin-bottom': '20mm', 'margin-left': '20mm', 'margin-right': '20mm',
        'minimum-font-size': '16', 'enable-local-file-access': '', 'dpi': '300',
    }

    config = pdfkit.configuration()
    pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)


# ---------- HTML EDITOR ----------
class InsertLinkDialog(QDialog):
    def __init__(self, selected_text=""):
        super().__init__()
        self.setWindowTitle("Insert Link")
        self.layout = QFormLayout(self)
        self.url_input = QLineEdit(self)
        self.text_input = QLineEdit(self)
        self.text_input.setText(selected_text)

        self.layout.addRow(QLabel("URL:"), self.url_input)
        self.layout.addRow(QLabel("Link Text:"), self.text_input)

        self.button_box = QHBoxLayout()
        insert_btn = QPushButton("Insert")
        cancel_btn = QPushButton("Cancel")
        insert_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        self.button_box.addWidget(insert_btn)
        self.button_box.addWidget(cancel_btn)
        self.layout.addRow(self.button_box)

    def get_data(self):
        return self.url_input.text(), self.text_input.text()


class HTMLEditor(QWidget):
    def __init__(self, html_path):
        super().__init__()
        self.html_path = html_path
        self.setWindowTitle("HTML Editor")
        self.resize(1000, 700)

        self.layout = QVBoxLayout(self)
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(self.html_path)))
        self.layout.addWidget(self.web_view)

        self.toolbar = QHBoxLayout()
        self.add_toolbar_buttons()
        self.layout.addLayout(self.toolbar)

        save_button = QPushButton("Save and Close")
        save_button.clicked.connect(self.save_html)
        self.layout.addWidget(save_button)

    def add_toolbar_buttons(self):
        buttons = {
            "Bold": "bold", "Italic": "italic", "Underline": "underline", "Strikethrough": "strikeThrough",
            "H1": "formatBlock|<h1>", "H2": "formatBlock|<h2>", "H3": "formatBlock|<h3>",
            "Ordered List": "insertOrderedList", "Unordered List": "insertUnorderedList",
            "Indent": "indent", "Outdent": "outdent",
            "Align Left": "justifyLeft", "Align Center": "justifyCenter", "Align Right": "justifyRight",
            "Undo": "undo", "Redo": "redo",
            "Insert Link": "insertLink"
        }
        for label, cmd in buttons.items():
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, c=cmd: self.execute_command(c))
            self.toolbar.addWidget(btn)

    def execute_command(self, command):
        if command == "insertLink":
            self.insert_link()
        elif "formatBlock" in command:
            tag = command.split("|")[1]
            self.run_js(f"document.execCommand('formatBlock', false, '{tag}');")
        else:
            self.run_js(f"document.execCommand('{command}');")

    def insert_link(self):
        self.web_view.page().runJavaScript('window.getSelection().toString()', self.handle_selected_text)

    def handle_selected_text(self, selected_text):
        dialog = InsertLinkDialog(selected_text)
        if dialog.exec_() == QDialog.Accepted:
            url, text = dialog.get_data()
            if url and text:
                self.run_js(f"document.execCommand('insertHTML', false, '<a href=\"{url}\">{text}</a>');")

    def run_js(self, js_code):
        self.web_view.page().runJavaScript(js_code)

    def save_html(self):
        self.web_view.page().toHtml(self.save_to_file)

    def save_to_file(self, html_content):
        with open(self.html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        QMessageBox.information(self, "Saved", f"HTML content saved to {self.html_path}")
        self.close()


def edit_html_content(html_path):
    app = QApplication(sys.argv)
    editor = HTMLEditor(html_path)
    editor.show()
    app.exec_()