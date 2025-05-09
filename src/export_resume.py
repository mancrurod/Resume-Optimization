import sys
import os
import re
import markdown2
import pdfkit
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, 
    QHBoxLayout, QLineEdit, QDialog, QFileDialog, QFormLayout, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# -------------------- UTILITIES --------------------

def remove_code_block_wrapper(md_text: str) -> str:
    """
    Remove surrounding triple backticks if the content is wrapped as a code block.
    """
    lines = md_text.strip().splitlines()
    if lines and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return "\n".join(lines[1:-1]).strip()
    return md_text

def normalize_markdown(md_text: str) -> str:
    """
    Normalize whitespace in Markdown lines.
    """
    lines = md_text.splitlines()
    return "\n".join(line.strip() for line in lines)

# -------------------- MARKDOWN TO HTML --------------------

def convert_md_to_html(md_path: str, html_path: str, for_editor: bool = False):
    """
    Convert a Markdown (.md) file into a styled HTML document.

    Parameters:
        md_path (str): Path to the input Markdown file.
        html_path (str): Path to save the resulting HTML file.
    """
    # Check if the Markdown file exists
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    # Read the Markdown file content
    with open(md_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Remove code block wrappers and normalize whitespace
    md_content = remove_code_block_wrapper(md_content)
    md_content = normalize_markdown(md_content)

    # Parse the header (name, role, contact info) and body content
    lines = md_content.strip().splitlines()
    name, role, contact_lines = "", "", []
    i = 0

    # Extract name (if it starts with "# ")
    if lines and lines[0].startswith("# "):
        name = lines[0][2:].strip()
        i += 1

    # Extract role (if it is surrounded by "**")
    if i < len(lines) and lines[i].startswith("**") and lines[i].endswith("**"):
        role = lines[i].strip("*").strip()
        i += 1

    # Extract contact information until a section header (##) is found
    while i < len(lines) and lines[i].strip() and not lines[i].startswith("##"):
        contact_lines.append(lines[i].strip())
        i += 1

    # Ensure proper spacing between blocks for correct HTML conversion
    content = "\n".join(lines[i:])
    content = re.sub(r'\n(?=\S)', '\n\n', content)
    html_body = markdown2.markdown(content, extras=[
        "fenced-code-blocks", "tables", "strike", "cuddled-lists", "metadata", "footnotes"
    ])


    # Compose the header HTML
    header_html = ""
    if name:
        header_html += f"<h1>{name}</h1>\n"
    if role:
        header_html += f"<p><strong>{role}</strong></p>\n"
    for line in contact_lines:
        line = line.strip()
        if not line:
            continue
        elif line.startswith("[[CONTACT]]"):
            clean = line.replace("[[CONTACT]]", "").strip()

            # If the line contains a link, convert it to HTML
            if "[" in clean and "](" in clean:
                rendered = markdown2.markdown(clean).strip()
                if rendered.startswith("<p>") and rendered.endswith("</p>"):
                    rendered = rendered[3:-4]  # elimina <p> envolvente
                header_html += f'<p class="contact">{rendered}</p>\n'
            else:
                header_html += f'<p class="contact">{clean}</p>\n'

    body_font = "Georgia, serif" if for_editor else "'Source Sans 3', sans-serif"
    header_font = "Georgia, serif" if for_editor else "'Garamond Premier Pro', serif"
    line_height = "1.4" if not for_editor else "1.6"

    html_document = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resume</title>
<style>
    /* === Fonts === */
    @font-face {{
        font-family: 'Garamond Premier Pro';
        src: url('../assets/fonts/GaramondPremrPro.otf') format('opentype');
        font-weight: normal;
        font-style: normal;
    }}
    @font-face {{
        font-family: 'Garamond Premier Pro';
        src: url('../assets/fonts/GaramondPremrPro-Bd.otf') format('opentype');
        font-weight: bold;
        font-style: normal;
    }}
    @font-face {{
        font-family: 'Garamond Premier Pro Subhead';
        src: url('../assets/fonts/GaramondPremrPro-Subh.otf') format('opentype');
        font-weight: normal;
        font-style: normal;
    }}
    @font-face {{
        font-family: 'Source Sans 3';
        src: url('../assets/fonts/SourceSans3-Regular.ttf') format('truetype');
        font-weight: 100 900;
        font-style: normal;
    }}

    /* === Base === */
    body {{
        font-family: {body_font};
        font-size: 11pt;
        line-height: {line_height};
        margin: 2em auto;
        max-width: 800px;
        color: #222;
        text-align: left;
    }}

    /* === Headings === */
    h1 {{
        font-family: {header_font}, serif;
        font-size: 15pt;
        font-weight: bold;
        margin-top: 1em;
        margin-bottom: 0.3em;
        text-align: center;
        color: #111;
    }}
    h2 {{
        font-family: 'Garamond Premier Pro Subhead', serif;
        font-size: 13pt;
        margin-top: 1.2em;
        margin-bottom: 0.3em;
        color: #111;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        border-bottom: 1px solid #ccc;
    }}

    /* === Content === */
    p, li {{
        margin-bottom: 0.4em;
        line-height: 1.3;
    }}

    ul, ol {{
        padding-left: 2em;              /* Indent list items */
        margin-top: 0.2em;              /* Space before the list */
        margin-bottom: 0.6em;           /* Space after the list */
    }}

    ul li, ol li {{
        margin-top: 0;
        margin-bottom: 0.1em;           /* Tight spacing between bullets */
        padding: 0;
    }}

    /* Fix extra spacing when <li> contains a <p> */
    li > p {{
        margin: 0.1em;                      /* Remove internal paragraph spacing */
        line-height: 1.3;               /* Consistent line spacing inside bullets */
    }}

    strong, b {{
        font-weight: 700;
    }}

    em, i {{
        font-style: italic;
    }}

    .contact {{
        font-family: 'Garamond Premier Pro', serif;
        font-weight: bold;
        font-size: 13pt;
        margin-bottom: 0.3em;
    }}

    /* === Links === */
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
<div class="resume-container">
  <div class="header" style="text-align: center; margin-bottom: 1.5em;">
    {header_html}
  </div>
  <div class="main">
    {html_body}
  </div>
</div>
</body>
</html>"""

    # Save the HTML content to the specified file
    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_document)


# -------------------- HTML TO PDF --------------------

def convert_html_to_pdf(html_path: str, pdf_path: str) -> None:
    """
    Convert an HTML file to a styled PDF using pdfkit.

    Parameters:
        html_path (str): Input HTML file.
        pdf_path (str): Output PDF path.
    """
    # Check if the HTML file exists
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    # Define PDF conversion options
    options = {
        'encoding': 'UTF-8',
        'page-size': 'A4',
        'margin-top': '12.7mm',
        'margin-bottom': '12.7mm',
        'margin-left': '12.7mm',
        'margin-right': '12.7mm',
        'minimum-font-size': '14',
        'enable-local-file-access': '',
        'dpi': '300',
    }

    # Configure pdfkit and generate the PDF
    config = pdfkit.configuration()
    pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)


# -------------------- HTML EDITOR --------------------

class InsertLinkDialog(QDialog):
    """
    Dialog to insert a hyperlink with custom URL and anchor text.
    """
    def __init__(self, selected_text=""):
        super().__init__()
        self.setWindowTitle("Insert Link")
        self.layout = QFormLayout(self)
        self.url_input = QLineEdit(self)  # Input field for the URL
        self.text_input = QLineEdit(self)  # Input field for the link text
        self.text_input.setText(selected_text)

        # Add input fields to the dialog layout
        self.layout.addRow(QLabel("URL:"), self.url_input)
        self.layout.addRow(QLabel("Link Text:"), self.text_input)

        # Add buttons for inserting or canceling
        self.button_box = QHBoxLayout()
        insert_btn = QPushButton("Insert")
        cancel_btn = QPushButton("Cancel")
        insert_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        self.button_box.addWidget(insert_btn)
        self.button_box.addWidget(cancel_btn)
        self.layout.addRow(self.button_box)

    def get_data(self):
        """
        Retrieve the entered URL and link text.
        """
        return self.url_input.text(), self.text_input.text()


class HTMLEditor(QWidget):
    """
    Full-featured HTML editor using PyQt5 with formatting toolbar.
    """
    def __init__(self, html_path):
        super().__init__()
        self.html_path = html_path  # Path to the HTML file being edited
        self.setWindowTitle("HTML Editor")
        self.resize(1000, 700)

        # Main layout for the editor
        self.layout = QVBoxLayout(self)
        self.web_view = QWebEngineView()  # Web view to display and edit HTML
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(self.html_path)))
        self.web_view.page().loadFinished.connect(self.enable_style_with_css)
        self.layout.addWidget(self.web_view)

        # Toolbar for formatting options
        self.toolbar = QHBoxLayout()
        self.add_toolbar_buttons()
        self.layout.addLayout(self.toolbar)

        # Save button to save changes and close the editor
        save_button = QPushButton("Save and Close")
        save_button.clicked.connect(self.save_html)
        self.layout.addWidget(save_button)

    def add_toolbar_buttons(self):
        """
        Add formatting buttons (bold, italic, lists, alignments, etc.)
        """
        buttons = {
            "Bold": "bold", "Italic": "italic", "Underline": "underline", "Strikethrough": "strikeThrough",
            "H1": "formatBlock|<h1>", "H2": "formatBlock|<h2>", "H3": "formatBlock|<h3>",
            "Ordered List": "insertOrderedList", "Unordered List": "insertUnorderedList",
            "Indent": "indent", "Outdent": "outdent",
            "Align Left": "justifyLeft", "Align Center": "justifyCenter", "Align Right": "justifyRight",
            "Undo": "undo", "Redo": "redo",
            "Insert Link": "insertLink",
            "Insert Image": "insertImage"
        }
        for label, cmd in buttons.items():
            btn = QPushButton(label)  # Create a button for each command
            btn.clicked.connect(lambda _, c=cmd: self.execute_command(c))  # Connect button to command execution
            self.toolbar.addWidget(btn)

    def execute_command(self, command):
        """
        Execute a formatting command on the HTML content.
        """
        if command == "insertLink":
            self.insert_link()
        elif command == "insertImage":
            self.insert_image()
        elif "formatBlock" in command:
            tag = command.split("|")[1]
            self.run_js(f"document.execCommand('formatBlock', false, '{tag}');")
        else:
            self.run_js(f"document.execCommand('{command}');")

    def insert_link(self):
        """
        Insert a hyperlink into the HTML content.
        """
        self.web_view.page().runJavaScript('window.getSelection().toString()', self.handle_selected_text)

    def handle_selected_text(self, selected_text):
        """
        Handle the selected text for inserting a hyperlink.
        """
        dialog = InsertLinkDialog(selected_text)
        if dialog.exec_() == QDialog.Accepted:
            url, text = dialog.get_data()
            if url and text:
                self.run_js(f"document.execCommand('insertHTML', false, '<a href=\"{url}\">{text}</a>');")

    def run_js(self, js_code):
        """
        Run JavaScript code in the web view.
        """
        self.web_view.page().runJavaScript(js_code)

    def save_html(self):
        """
        Save the edited HTML content to the file.
        """
        self.web_view.page().toHtml(self.save_to_file)

    def save_to_file(self, html_content):
        """
        Write the HTML content to the file and close the editor.
        """
        with open(self.html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        QMessageBox.information(self, "Saved", f"HTML content saved to {self.html_path}")
        self.close()

    def insert_image(self):
        """
        Open a file dialog to select an image and insert it into the HTML.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.gif)")
        if file_path:
            uri = QUrl.fromLocalFile(file_path).toString()
            img_tag = f'''
            <div style="float:right; margin: 0 0 10px 20px;">
                <img src="{uri}" alt="Profile Photo" style="max-width:150px; height:auto; border-radius:8px;">
            </div>
            '''
            self.run_js(f"document.execCommand('insertHTML', false, `{img_tag}`);")

    def enable_style_with_css(self):
        """
        Ensure formatting commands like Bold/Italic use inline styles.
        """
        js = "document.execCommand('styleWithCSS', false, true);"
        self.web_view.page().runJavaScript(js)



def edit_html_content(html_path: str) -> None:
    """
    Launch the HTML editor for manual visual editing.

    Parameters:
        html_path (str): Path to the HTML file to edit.
    """
    app = QApplication(sys.argv)  # Create the PyQt application
    editor = HTMLEditor(html_path)  # Initialize the HTML editor
    editor.show()  # Show the editor window
    app.exec_()  # Run the application event loop
