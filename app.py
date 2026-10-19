"""Streamlit UI for the University Document Assistant prototype."""
from io import BytesIO
from pathlib import Path
import streamlit as st
from pypdf import PdfReader
from retrieval import chunk_text, search

st.set_page_config(page_title='University Document Assistant', page_icon='📚', layout='wide')
st.title('University Document Assistant')
st.caption('Student project · local passage search · development prototype')
st.write('Upload a handbook, course notes, or public university document. Ask a question to find relevant passages with file and page references.')
st.info('This version retrieves original passages using keyword ranking. It does not generate answers, translate languages, or provide official university advice.')

with st.sidebar:
    st.header('Document collection')
    uploads = st.file_uploader('Upload PDF, TXT, or Markdown files', type=['pdf', 'txt', 'md'], accept_multiple_files=True)
    use_example = st.checkbox('Include the public Aror University example', value=True)
    top_k = st.slider('Passages to show', 1, 5, 3)
    st.caption('No external AI API is used. Files are processed in the running app; this app does not save uploads to disk. A hosting provider still controls the runtime. Use public or approved documents.')

passages = []
if use_example:
    sample = Path(__file__).parent / 'examples' / 'aror-university.txt'
    passages.extend(chunk_text(sample.read_text(encoding='utf-8'), sample.name))

if len(uploads) > 10:
    st.error('Please use at most 10 documents per session.')
    st.stop()

for upload in uploads:
    if upload.size > 10 * 1024 * 1024:
        st.warning(f'{upload.name}: skipped because it exceeds 10 MB.')
        continue
    try:
        if upload.name.lower().endswith('.pdf'):
            reader = PdfReader(BytesIO(upload.getvalue()))
            if reader.is_encrypted:
                st.warning(f'{upload.name}: encrypted PDFs are not supported.')
                continue
            if len(reader.pages) > 100:
                st.warning(f'{upload.name}: use a PDF with at most 100 pages.')
                continue
            found_text = False
            for page_number, page in enumerate(reader.pages, 1):
                text = page.extract_text() or ''
                found_text = found_text or bool(text.strip())
                passages.extend(chunk_text(text, upload.name, page_number))
            if not found_text:
                st.warning(f'{upload.name}: no extractable text found. Scanned PDFs need OCR, which this version does not include.')
        else:
            text = upload.getvalue().decode('utf-8-sig')
            passages.extend(chunk_text(text, upload.name))
    except Exception:
        st.warning(f'{upload.name}: could not read this file. Try an unencrypted text-based PDF or a UTF-8 text file.')

st.caption(f'{len(passages)} searchable passages · {len(set(p.source for p in passages))} document names')
if not passages:
    st.warning('Add a document or enable the example to begin.')
    st.stop()

question = st.text_input('What would you like to find?', placeholder='For example: machine learning computer vision')
if question.strip():
    results = search(question, passages, limit=top_k)
    if not results:
        st.warning('No sufficiently matching passage found. Try a more specific question using terms from your documents. This does not prove the information is absent.')
    else:
        st.subheader('Relevant passages')
        st.caption('These are excerpts, not generated answers. Check the original document and its publication date before relying on a passage.')
        export = []
        for index, result in enumerate(results, 1):
            passage = result.passage
            with st.container(border=True):
                st.markdown(f'**Source {index}**')
                st.text(f'{passage.source} · page {passage.page} · passage {passage.number}')
                st.write(passage.text)
                with st.expander('Retrieval details'):
                    st.caption(f'BM25 score: {result.score:.3f} · query-term coverage: {result.coverage:.0%}. Neither value is an accuracy or confidence estimate.')
            export.append(f'[{index}] {passage.source} | page {passage.page} | passage {passage.number}\n{passage.text}')
        st.download_button('Download cited passages', '\n\n'.join(export), file_name='document-passages.txt', mime='text/plain')
