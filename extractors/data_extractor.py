import fitz  # PyMuPDF
import camelot  # For table extraction

class DataExtractor:
    def __init__(self, pdf_loader):
        self.pdf_loader = pdf_loader
        self.pdf_file = pdf_loader.file_path

    def extract_text(self):
        # Text extraction logic (already implemented)
        reader = self.pdf_loader.load_file()
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def extract_images(self):
        images = []
        pdf_document = fitz.open(self.pdf_file)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                width, height = base_image["width"], base_image["height"]
                images.append({
                    "image_data": image_bytes,
                    "ext": image_ext,
                    "page": page_num + 1,
                    "dimensions": (width, height)
                })
        pdf_document.close()
        return images

    def extract_urls(self):
        urls = []
        pdf_document = fitz.open(self.pdf_file)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            links = page.get_links()
            for link in links:
                if "uri" in link:
                    url = link["uri"]
                    rect = link["from"]
                    urls.append({
                        "url": url,
                        "page": page_num + 1,
                        "position": {
                            "x0": rect.x0,
                            "y0": rect.y0,
                            "x1": rect.x1,
                            "y1": rect.y1
                        }
                    })
        pdf_document.close()
        return urls

    def extract_tables(self):
        """Extract tables from the PDF using Camelot."""
        tables = camelot.read_pdf(self.pdf_file, pages="all")
        table_data = []
        for table in tables:
            table_data.append(table.df)  # df is the table as a pandas DataFrame
        return table_data
