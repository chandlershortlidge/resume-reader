import fitz


def load_file(path: str) -> fitz.Document:
    doc = fitz.open(path)
    print(f"Loaded document with {doc.page_count} pages")
    return doc


def report_metadata(doc: fitz.Document) -> None:
    meta = doc.metadata
    for key, value in meta.items():
        print(f"{key}: {value}")
        
        
def highlight_keywords(doc: fitz.Documnt, kw_list: list[str]) -> fitz.Document:
    # multiple kw
    ...
    
    
def save_highlighted_doc(doc: fitz.Document) -> None:
    ...
    
    
def get_links(doc: fitz.Document) -> list[str]:
    """
    extracts links with http or https and returns the list of links
    """
    ...
    
    
def get_emails(doc: fitz.Document) -> list[str]:
    ...
    
    
def convert_to_markdown(doc: fitz.Document) -> str:
    # TODO
    # try your function
    # try als https://pymupdf.readthedocs.io/en/latest/rag.html
    ...