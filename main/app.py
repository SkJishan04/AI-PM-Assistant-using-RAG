import gradio as gr
from vector_store import clear_collection
from indexer import index_documents
from pipeline import answer_question

with gr.Blocks() as demo:
    gr.Markdown("# AI PM Assistant")
    gr.Markdown("Upload PRDs, meeting notes, or Jira exports. Then ask a question.")

    files = gr.File(
        label="Documents",
        file_count="multiple",
        file_types=[".txt", ".md", ".csv", ".pdf", ".docx"],
    )
    index_button = gr.Button("Index documents")
    index_status = gr.Textbox(label="Index status")

    question = gr.Textbox(label="Question", placeholder="What risks are mentioned in the PRD?")
    answer = gr.Textbox(label="Answer", lines=12)
    ask_button = gr.Button("Ask")

    index_button.click(index_documents, inputs=files, outputs=index_status)
    ask_button.click(answer_question, inputs=question, outputs=answer)

if __name__ == "__main__":
    demo.launch()