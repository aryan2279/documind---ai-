from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def create_chunks_with_pages(pages):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    final_chunks = []

    for page in pages:

        chunks = splitter.split_text(
            page["text"]
        )

        for chunk in chunks:

            final_chunks.append(
                {
                    "text": chunk,
                    "page": page["page"]
                }
            )

    return final_chunks