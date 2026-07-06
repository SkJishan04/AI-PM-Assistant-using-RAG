# AI PM Assistant (RAG)

A simple AI assistant for Product Managers. Upload your PRDs, meeting notes, or Jira exports, and ask questions about them in plain English. The app retrieves the most relevant pieces of your documents and uses an LLM to answer based only on that content.

Built with **Gradio**, **ChromaDB**, and **Sentence Transformers**, using a **Retrieval-Augmented Generation (RAG)** pipeline.

## How it works

1. **Upload documents** — supports `.txt`, `.md`, `.csv`, `.pdf`, `.docx`
2. **Indexing** — documents are split into small chunks and converted into embeddings, then stored in a local vector database (ChromaDB)
3. **Ask a question** — the app retrieves the most relevant chunks for your question
4. **Answer generation** — the retrieved chunks + your question are sent to an LLM (OpenAI or Gemini), which answers using only that context

## Project structure

```
main/
├── app.py            # Gradio UI (upload, index, ask, display answer)
├── config.py         # Settings (chunk size, top-k results, model name)
├── file_loader.py    # Reads txt/pdf/docx files into plain text
├── chunker.py        # Splits text into overlapping chunks
├── vector_store.py   # Sets up the ChromaDB collection
├── indexer.py        # Turns uploaded files into indexed chunks
├── retriever.py      # Finds the most relevant chunks for a question
├── llm.py            # Builds the prompt and calls the LLM
└── pipeline.py        # Full flow: question → retrieve → prompt → answer
```

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/AI-PM-Assistant-using-RAG.git
cd AI-PM-Assistant-using-RAG/main
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install gradio chromadb sentence-transformers pypdf python-docx openai google-generativeai
```

### 4. (Optional) Add an LLM API key
Without a key, the app still works — it will just show you the raw retrieved text instead of a generated answer.

```bash
export OPENAI_API_KEY="sk-..."
# or
export GEMINI_API_KEY="..."
```

### 5. Run the app
```bash
python app.py
```

Open the local URL Gradio prints in your terminal (usually `http://127.0.0.1:7860`).

## Usage

1. Upload one or more documents using the **Documents** panel
2. Click **Index documents** — wait for the status message confirming how many chunks were indexed
3. Type a question in the **Question** box
4. Click **Ask** — the answer appears below, along with the source chunks it was based on

## Configuration

You can tweak these in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `CHUNK_SIZE` | 900 | Max characters per chunk |
| `CHUNK_OVERLAP` | 150 | Overlap between consecutive chunks |
| `TOP_K` | 4 | Number of chunks retrieved per question |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model used for embeddings |

## Notes

- The vector database is stored locally in a `chroma_db/` folder — it persists between runs
- Supported LLM providers: OpenAI (`OPENAI_API_KEY`) and Google Gemini (`GEMINI_API_KEY`). If neither is set, the app falls back to showing retrieved context only
- This is an early-stage project — expect rough edges. Contributions and issues welcome

## Roadmap

- [ ] Add a "clear index" button in the UI
- [ ] Add a `requirements.txt`
- [ ] Handle scanned/image-based PDFs (OCR)
- [ ] Deploy to Hugging Face Spaces

## License

See [LICENSE](LICENSE).