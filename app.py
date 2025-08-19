import streamlit as st
import os
from pdf_processor import (
    load_file,
    pdf_to_markdown,
    highlight_keywords,
    save_highlighted_doc,
)
from scoring_processor import (
    load_keywords_from_config,
    normalize,
    calculate_score,
)

st.title("📄 Resume Reader & Scorer")

# Load keywords from config.json
# Using a cache to avoid reloading on every interaction
@st.cache_data
def get_keywords():
    try:
        return load_keywords_from_config("config.json")
    except FileNotFoundError:
        st.error(
            "config.json not found. Please create it with 'required_keywords' and 'optional_keywords'."
        )
        return [], []


def get_score_color(percentage: float) -> str:
    """
    Returns a color string based on the score percentage.
    Colors are chosen for readability on a light background.
    """
    if percentage >= 75:
        return "green"
    elif percentage >= 50:
        return "orange"  # Using orange instead of yellow for better contrast
    elif percentage >= 25:
        return "darkorange"
    else:
        return "red"


def get_score_description(percentage: float) -> str:
    """Returns a descriptive string based on the score percentage."""
    if percentage >= 75:
        return "— Great match"
    elif percentage >= 50:
        return "— Good match"
    elif percentage >= 25:
        return "— Okay match"
    else:
        return "— Poor match"


required_keywords, optional_keywords = get_keywords()

uploaded_file = st.file_uploader("Upload a resume (PDF)", type="pdf")

if uploaded_file is not None:
    # To work with your existing pdf_processor functions,
    # we can save the uploaded file to a temporary location.
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Successfully uploaded '{uploaded_file.name}'")

    try:
        # --- Processing and Scoring ---
        with st.spinner("Processing and scoring resume..."):
            # 1. Load and process the PDF
            doc = load_file(file_path)
            markdown_text = pdf_to_markdown(doc)
            clean_text = normalize(markdown_text)

            # 2. Calculate the score
            score, found_terms, max_score = calculate_score(
                clean_text, required_keywords, optional_keywords
            )
            all_keywords = required_keywords + optional_keywords
    except OSError as e:
        st.error(e)
        st.stop()

    # --- Display Results ---
    st.header("Scoring Results")

    # Calculate percentage and determine color
    percentage_score = (score / max_score) * 100 if max_score > 0 else 0
    color = get_score_color(percentage_score)
    description = get_score_description(percentage_score)

    # Display the colored score using custom HTML
    st.markdown(f"""
    <p style="font-size: 0.875rem; color: #808495; margin-bottom: -5px;">Match Score</p>
    <div style="display: flex; align-items: baseline; gap: 10px;">
        <p style="font-size: 2.25rem; font-weight: 600; color: {color}; margin: 0;">{percentage_score:.1f}%</p>
        <p style="font-size: 1.25rem; font-weight: 500; color: {color}; margin: 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("See keyword analysis"):
        st.write("**Keywords found:**")
        st.write(", ".join(sorted(list(found_terms))) or "None")

        missing_keywords = set(all_keywords) - found_terms
        st.write("**Keywords missing:**")
        st.write(", ".join(sorted(list(missing_keywords))) or "None")

    # --- Highlight and Download ---
    st.header("Highlighted resume")
    with st.spinner("Generating highlighted PDF..."):
        # 1. Highlight keywords in the document
        highlighted_doc = highlight_keywords(doc, list(found_terms))

        # 2. Save the highlighted document to a temporary path
        highlighted_path = os.path.join(temp_dir, f"highlighted_{uploaded_file.name}")
        save_highlighted_doc(highlighted_doc, highlighted_path)

        # 3. Provide a download button
        with open(highlighted_path, "rb") as f:
            st.download_button(
                label="Download highlighted PDF",
                data=f,
                file_name=f"highlighted_{uploaded_file.name}",
                mime="application/pdf",
            )