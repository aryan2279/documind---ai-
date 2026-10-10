import fitz


def extract_text_with_pages(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_number in range(len(document)):

        page = document.load_page(
            page_number
        )

        text = page.get_text()

        if text.strip():

            pages.append(
                {
                    "page": page_number + 1,
                    "text": text
                }
            )

    return pages