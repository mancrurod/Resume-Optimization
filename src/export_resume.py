import sys
import os
from markdown_it import MarkdownIt
import pdfkit
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, 
    QHBoxLayout, QLineEdit, QDialog, QFormLayout, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


# Utility Functions
def convert_md_to_html(md_path, html_path):
    """Convert Markdown to HTML while preserving formatting."""
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    with open(md_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Initialize markdown-it parser
    md = MarkdownIt("commonmark", {"breaks": True})

    # Convert markdown to HTML using markdown-it-py
    html_content = md.render(md_content)

    # Wrap the content in a basic HTML structure
    html_document = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Resume</title>
        <style>
            body {{
                font-family: Helvetica, sans-serif;
                font-size: 16px;
                line-height: 1.6;
                margin: 2em;
                max-width: 800px;
            }}
            h1, h2, h3 {{
                color: #333;
            }}
            a {{
                color: #0066cc;
                text-decoration: none;
            }}
            ul {{
                padding-left: 40px;
            }}
            ul li {{
                list-style-type: disc;
                margin-bottom: 5px;
            }}
            ol {{
                padding-left: 40px;
            }}
            ol li {{
                list-style-type: decimal;
                margin-bottom: 5px;
            }}
        </style>
    </head>
    <body contenteditable="true">
        {html_content}
    </body>
    </html>"""

    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_document)

def convert_html_to_pdf(html_path, pdf_path):
    """Convert HTML to PDF."""
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    options = {
        'encoding': 'UTF-8', 'page-size': 'A4', 'margin-top': '20mm',
        'margin-bottom': '20mm', 'margin-left': '20mm', 'margin-right': '20mm',
        'minimum-font-size': '16', 'enable-local-file-access': '', 'dpi': '300',
    }

    try:
        config = pdfkit.configuration()
        pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)
    except Exception as e:
        print(f"PDF conversion failed: {e}")
        raise


# Dialog Classes
class InsertLinkDialog(QDialog):
    """A dialog to input URL and Link Text for inserting a link."""
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
        self.insert_button = QPushButton("Insert", self)
        self.insert_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.button_box.addWidget(self.insert_button)
        self.button_box.addWidget(self.cancel_button)

        self.layout.addRow(self.button_box)

    def get_data(self):
        """Return URL and Link Text from the dialog."""
        return self.url_input.text(), self.text_input.text()


# Editor Classes
class HTMLEditor(QWidget):
    """A robust WYSIWYG HTML editor."""
    def __init__(self, html_path):
        super().__init__()
        self.html_path = html_path
        self.setWindowTitle("HTML Editor")
        self.resize(1000, 700)

        self.layout = QVBoxLayout(self)
        self.web_view = QWebEngineView(self)
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(self.html_path)))
        self.layout.addWidget(self.web_view)

        self.toolbar = QHBoxLayout()
        self.add_toolbar_buttons()
        self.layout.addLayout(self.toolbar)

        self.btn_save = QPushButton("Save and Close", self)
        self.btn_save.clicked.connect(self.save_html)
        self.layout.addWidget(self.btn_save)

    def add_toolbar_buttons(self):
        """Add buttons to the toolbar."""
        buttons = {
            "Bold": "bold", "Italic": "italic", "Underline": "underline", "Strikethrough": "strikeThrough",
            "H1": "formatBlock|<h1>", "H2": "formatBlock|<h2>", "H3": "formatBlock|<h3>",
            "Ordered List": "insertOrderedList", "Unordered List": "insertUnorderedList",
            "Indent": "indent", "Outdent": "outdent",
            "Align Left": "justifyLeft", "Align Center": "justifyCenter", "Align Right": "justifyRight",
            "Undo": "undo", "Redo": "redo",
            "Insert Link": "insertLink"
        }
        for label, command in buttons.items():
            self.add_toolbar_button(label, command)

    def add_toolbar_button(self, label, command):
        """Add a button to the toolbar.""" 
        btn = QPushButton(label, self)
        btn.clicked.connect(lambda: self.execute_command(command))
        self.toolbar.addWidget(btn)

    def execute_command(self, command):
        """Execute the corresponding command using JavaScript."""
        if command == "insertLink":
            self.insert_link()
        elif "formatBlock" in command:
            tag = command.split("|")[1]
            self.run_js(f"document.execCommand('formatBlock', false, '{tag}');")
        else:
            self.run_js(f"document.execCommand('{command}');")

    def run_js(self, js_code):
        """Run JavaScript code in the web view.""" 
        self.web_view.page().runJavaScript(js_code)

    def insert_link(self):
        """Open a dialog to insert a link and populate the editor.""" 
        self.web_view.page().runJavaScript('window.getSelection().toString()', self.handle_selected_text)

    def handle_selected_text(self, selected_text):
        """Handle selected text and open the InsertLinkDialog.""" 
        dialog = InsertLinkDialog(selected_text)
        if dialog.exec_() == QDialog.Accepted:
            url, text = dialog.get_data()
            if url and text:
                self.run_js(f"document.execCommand('insertHTML', false, '<a href=\"{url}\">{text}</a>');")

    def save_html(self):
        """Save the current HTML content.""" 
        self.web_view.page().toHtml(self.save_to_file)

    def save_to_file(self, html_content):
        """Write the HTML content to the file.""" 
        with open(self.html_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        QMessageBox.information(self, "Saved", f"HTML content saved to {self.html_path}")
        self.close()


# Main Functionality
def edit_html_content(html_path):
    """Launch the HTML editor.""" 
    app = QApplication(sys.argv)
    editor = HTMLEditor(html_path)
    editor.show()
    app.exec_()


if __name__ == "__main__":
    md_path = "example.md"
    html_path = "example.html"
    pdf_path = "example.pdf"

    convert_md_to_html(md_path, html_path)
    edit_html_content(html_path)
    convert_html_to_pdf(html_path, pdf_path)
