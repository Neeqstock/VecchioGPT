import fitz  # PyMuPDF
from openai import OpenAI
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text


# Function to split text into chunks
def split_text_into_chunks(text, max_tokens=8192):
    sentences = text.split(". ")
    chunks = []
    current_chunk = []

    for sentence in sentences:
        current_chunk.append(sentence)
        if len(" ".join(current_chunk)) > max_tokens:
            chunks.append(" ".join(current_chunk[:-1]))
            current_chunk = [sentence]

    chunks.append(" ".join(current_chunk))  # Add the last chunk
    return chunks


# Function to generate embeddings for chunks
def generate_embeddings_for_chunks(chunks, api_key):
    embeddings = []

    for chunk in chunks:
        response = client.embeddings.create(input=chunk, model="text-embedding-ada-002")
        embeddings.append(response.data[0].embedding)

    return embeddings


# Function to ask a question with context
def ask_question_with_context(chunks, question, api_key):
    context = " ".join(chunks)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Here is some context:\n\n{context}\n\nQuestion: {question}",
            },
        ],
        max_tokens=150,
    )
    return response.choices[0].message.content


# Example usage
api_key = ""
client = OpenAI(api_key=api_key)

Tk().withdraw()  # Hide the root window
pdf_path = askopenfilename(
    title="Select a PDF file", filetypes=[("PDF files", "*.pdf")]
)

text = extract_text_from_pdf(pdf_path)
chunks = split_text_into_chunks(text, max_tokens=8192)
embeddings = generate_embeddings_for_chunks(chunks, api_key)
question = "What is the main topic of this document?"

answer = ask_question_with_context(chunks, question, api_key)
print(answer)
