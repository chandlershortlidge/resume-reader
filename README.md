# Resume Reader & Scorer

This project is a Streamlit application designed to score resumes against a predefined set of keywords and highlight the found keywords in the uploaded PDF.

## Features
- **PDF Processing**: The application can load PDF files, extract text, and convert it to a markdown format for processing.
- **Keyword Scoring**: It calculates a match score for a resume based on a configurable list of required and optional keywords. Required keywords are weighted with a higher value (1 point) than optional keywords (0.5 points).
- **Keyword Highlighting**: It generates a new PDF where all found keywords are highlighted for easy visualization.
- **Match Analysis**: The application reports a percentage match score and lists all found and missing keywords.
- **Downloadable Output**: The highlighted resume can be downloaded directly from the application.

## Setup and Installation

### Prerequisites
The project requires Python version 3.12 or higher.

### Dependencies
The dependencies are managed using `pyproject.toml` and `uv.lock`. You will need to install `uv` to manage the packages, or use `pip`.

The main dependencies include:
- `en-core-web-sm`: A small English language model from spaCy.
- `pymupdf`: For processing PDF files.
- `spacy`: For advanced natural language processing tasks, specifically the PhraseMatcher.
- `streamlit`: To run the web application.

A crucial step is to download the spaCy model. You must run the following command in your activated Python environment after installing the dependencies:

```bash
python -m spacy download en_core_web_sm
```

## Usage

### Configure Keywords
Before running the application, you must define the keywords you want to match in the `config.json` file. The file should contain two lists, `required_keywords` and `optional_keywords`.

Example `config.json`:
```json
{
  "required_keywords": [
    "LLMs", "prompt engineering", "embeddings", "RAG workflows",
    "Python", "LangChain", "spaCy", "knowledge extraction", "Data Scientist"
  ],
  "optional_keywords": [
    "TensorFlow", "Keras", "PyTorch", "vector database",
    "SQL", "Pandas", "FAISS", "document AI"
  ]
}
```

### Run the Application
Navigate to the project directory and run the `app.py` file using Streamlit:

```bash
streamlit run app.py
```

### Upload a Resume
The Streamlit interface will prompt you to upload a PDF file. Once uploaded, the application will process the resume, score it, and display the results. You can then download the highlighted PDF.

## Project Structure
- `app.py`: The main Streamlit application script.
- `scoring_processor.py`: Contains the core logic for keyword loading, text normalization, and score calculation.
- `pdf_processor.py`: Handles all PDF-related tasks, including loading, text extraction, highlighting, and saving.
- `config.json`: The configuration file for defining required and optional keywords.
- `KANDACE_LOUDOR_new.md`: A sample resume file in markdown format.
- `pyproject.toml`: Project configuration and dependency manifest.
- `.python-version`: Specifies the Python version to be used.
- `.gitignore`: Specifies files and directories to be ignored by Git.
