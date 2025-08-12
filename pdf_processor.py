import fitz
import re


def load_file(path: str) -> fitz.Document:
    doc = fitz.open(path)
    print(f"Loaded document with {doc.page_count} pages")
    return doc


def report_metadata(doc: fitz.Document) -> None:
    meta = doc.metadata
    for key, value in meta.items():
        print(f"{key}: {value}")
        
        
def highlight_keywords(doc: fitz.Document, kw_list: list[str]) -> fitz.Document:
    # Loop through each page in the document
    for page in doc:
          # Loop through each keyword in the provided list (kw_list)
        for keyword in kw_list:
            # Search for the current keyword on the page
            matches = page.search_for(keyword)
            if matches:
                print(f"Found '{keyword}' on page {page.number + 1}")
                # For each match, add a highlight
                for r in matches:
                    highlight = page.add_highlight_annot(r)
                    highlight.update()
    return doc
    
    
def save_highlighted_doc(doc: fitz.Document, out_path: str = "highlighted_output.pdf") -> None:
    """Saves the document to the specified path."""
    doc.save(out_path, garbage=4, deflate=True, clean=True)
    print(f"Saved highlighted PDF as: {out_path}")
    
    
    
def get_links(doc: fitz.Document) -> list[str]:
    """
    extracts links with http or https and returns the list of links
    """
    ...
    
    
def get_emails(doc: fitz.Document) -> list[str]:
    ...
    
    
def pdf_to_markdown(doc: fitz.Document) -> str:
    
    md_lines = []

    for p in range(doc.page_count):
        page = doc.load_page(p)
        # get a nested dict of blocks → lines → spans
        page_dict = page.get_text("dict")

        for block in page_dict["blocks"]:
            # Only text blocks (ignore images, drawings)
            if block["type"] != 0:
                continue

            # Join all spans in this block into one text string
            text = " ".join(span["text"] for line in block["lines"] for span in line["spans"])
            text = text.strip()
            if not text:
                continue

            #  Simple heuristic: ALL CAPS + short → H2
            if text.isupper() and len(text) < 60:
                md_lines.append(f"## {text.title()}")
                continue

            # Detect bullet lists (e.g. lines starting with • or –)
            if re.match(r"^[•\-\u2022]\s+", text):
                item = re.sub(r"^[•\-\u2022]\s+", "", text)
                md_lines.append(f"-{item}")
                continue

            # Otherwise treat as paragraph
            md_lines.append(text)

        # Add a page break marker (optional)
        md_lines.append("\n---\n")
    
    return "\\n\\n".join(md_lines)    

