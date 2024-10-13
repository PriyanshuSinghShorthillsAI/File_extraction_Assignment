import os
from loaders.pdf_loader import PDFLoader
from extractors.data_extractor import DataExtractor
from storage.file_storage import FileStorage
import fitz  # PyMuPDF

def main():
    pdf_file = "sample.pdf"  

    # Create a PDFLoader instance
    pdf_loader = PDFLoader(pdf_file)

    # Validate the PDF file
    pdf_loader.validate_file()

    # Extract data from the PDF
    extractor = DataExtractor(pdf_loader)
    pdf_text = extractor.extract_text()
    images = extractor.extract_images()
    urls = extractor.extract_urls()
    tables = extractor.extract_tables()  # Extract tables from the PDF

    # Close the file after processing
    pdf_loader.close_file()

    # Create a folder for storing the extracted data
    pdf_base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    output_dir = os.path.join("extracted_data", pdf_base_name)
    file_storage = FileStorage(output_dir)

    # Save the extracted data
    file_storage.save(pdf_text, os.path.basename(pdf_file), 'text')
    file_storage.save(images, os.path.basename(pdf_file), 'image')
    file_storage.save(urls, os.path.basename(pdf_file), 'url')
    file_storage.save(tables, os.path.basename(pdf_file), 'table')  # Save tables

    print(f"Extracted data saved to: {output_dir}")

if __name__ == "__main__":
    main()
