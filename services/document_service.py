from pypdf import PdfReader
from core.rag import create_chunks, create_vector_store


class DocumentService:

    def process_files(self, uploaded_files):

        all_chunks = []

        for file in uploaded_files:
            reader = PdfReader(file)

            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()

                if page_text:
                    chunks = create_chunks(page_text)

                    for c in chunks:
                        c["source"] = file.name
                        c["page"] = page_num + 1

                    all_chunks.extend(chunks)

        index, embeddings = create_vector_store(all_chunks)

        return all_chunks, index, embeddings