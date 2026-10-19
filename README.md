# University Document Assistant

A student-project prototype for finding cited passages in university documents. It connects text processing, information retrieval, and a simple interactive interface.

**Status:** first implementation; in development. This is independently developed student work, not an official Aror University service.

## What works in this version

- Upload up to 10 PDF, UTF-8 TXT, or Markdown documents.
- Extract text and split it into overlapping passages while retaining file/page references.
- Rank matching passages with a small BM25 implementation.
- Display original passages and export cited results as plain text.
- Explore a small, source-linked public Aror University example.
- Search Unicode text, including Urdu words; no cross-language translation is provided.

This is a retrieval assistant, not a generative chatbot or a completed RAG system. It uses no external AI API and needs no paid model subscription.

## Run locally

Use Python 3.10 or newer:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local address printed by Streamlit. Enable the example or upload a document, then try `machine learning computer vision`.

## Project structure

| Path | Purpose |
| --- | --- |
| `app.py` | Upload, PDF extraction, search interface, cited result export |
| `retrieval.py` | Unicode tokenization, passage chunking, BM25 ranking |
| `examples/aror-university.txt` | Small public example with official-source links |
| `tests/test_retrieval.py` | Retrieval, abstention, Unicode, and citation tests |
| `requirements.txt` | UI and PDF dependencies |

## Verification

```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py retrieval.py
```

Core retrieval tests run without third-party dependencies. UI and PDF behavior additionally require installed packages and a manual run. No accuracy benchmark or deployment is claimed.

## Limitations

- Keyword retrieval can miss paraphrases, misspellings, and cross-language questions.
- Matching passages are excerpts, not verified answers. Ranking scores are not confidence scores.
- Scanned PDFs require OCR, which is not included. Encrypted PDFs are not supported.
- Files are limited to 10 MB and PDFs to 100 pages; extraction time still varies with content.
- Uploaded content is processed by the app without writing upload files to disk or sending them to an AI provider. Hosting and runtime operators still control the environment.
- Use public or approved documents. Review dates and original sources for policy questions.
- Duplicate upload filenames have ambiguous source names; rename files uniquely before upload.

## Academic connection and next steps

This project practices NLP preprocessing, information retrieval, data structures, interface development, and evaluating whether a system should abstain. Future work can add labeled retrieval questions, OCR, semantic embeddings, and optional grounded answer generation, each with its own evaluation.

The Aror AI program includes NLP, machine learning, computer vision, and ethical AI topics. This project is aligned with those areas, but is not claimed as a university-assigned or graded submission.

Official context: [University](https://aror.edu.pk/) · [AI program](https://newsite.aror.edu.pk/faculty-fest/artificial-intelligence/).

## Development provenance

The initial implementation was prepared with AI coding assistance in October 2026. The repository owner should review the code, run the interface, extend the evaluation, and document their own contribution before presenting it as independently authored work or submitting it for academic credit.
