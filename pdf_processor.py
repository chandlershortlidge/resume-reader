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
    

def save_markdown_file(markdown_text: str, file_path: str):
    """Saves a string of markdown text to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    print(f"Markdown content successfully saved to {file_path}")
    
        
    
def get_links(doc: fitz.Document) -> list[str]:
    """
    extracts links with http or https and returns the list of links
    """
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num) 
        links = page.links() # list of link-dicts from page

        if not links:
            continue

        print(f"Page {page_num + 1} links:")
        for link in links: 
        # Common keys: 'kind', 'from', and either 'uri' or 'xref'/'to'
            kind = link["kind"]
            location = link["from"] # where the link is located
            uri = link.get("uri") # external URL, if any
            to = link.get("to") # (page, ...) for internal jumps

            if uri:
                print(f"  -> URI: {uri}")
            elif to:
                print(f"  → Internal link to page {to[0] + 1}")
            else:
                print("  → Other link kind:", kind)

            print(f"    location on page: {location}")   
 
    
    
def get_emails(doc: fitz.Document) -> list[str]:
    ...
    
    
def pdf_to_markdown(doc: fitz.Document) -> str:
    md_lines = []

    for page in doc:
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
        md_lines.append("---")
    
    # Corrected return statement with single backslashes
    return "\n\n".join(md_lines)   

