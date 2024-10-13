import os
from loaders.pdf_loader import PDFLoader
from loaders.docx_loader import DOCXLoader
from loaders.ppt_loader import PPTLoader
from extractors.data_extractor import DataExtractor
from storage.file_storage import FileStorage

def main():
    file_path = "sample.pdf"  # Change this to the file you want to process

    # Determine the file type and use the appropriate loader
    if file_path.endswith(".pdf"):
        loader = PDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = DOCXLoader(file_path)
    elif file_path.endswith(".pptx"):
        loader = PPTLoader(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX, or PPTX.")

    # Validate the file (ensures it's the correct type)
    loader.validate_file()

    # Load the file using the appropriate loader
    loader.load_file()

    # Create an instance of DataExtractor for extracting content
    extractor = DataExtractor(loader)

    # Extract text from the file
    extracted_text = extractor.extract_text()

    # Extract images (if available)
    images = extractor.extract_images()

    # Extract URLs (if it's a PDF or DOCX)
    urls = extractor.extract_urls() if file_path.endswith(('.pdf', '.docx')) else None

    # Extract tables (for PDFs or DOCX only)
    tables = extractor.extract_tables() if file_path.endswith(('.pdf', '.docx')) else None

    # Close the file (if applicable)
    if hasattr(loader, 'close_file'):
        loader.close_file()

    # Create a folder for storing the extracted data
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join("extracted_data", base_name)
    file_storage = FileStorage(output_dir)

    # Save the extracted text
    file_storage.save(extracted_text, os.path.basename(file_path), 'text')

    # Save the extracted images
    if images:
        file_storage.save(images, os.path.basename(file_path), 'image')

    # Save the extracted URLs (if any)
    if urls:
        file_storage.save(urls, os.path.basename(file_path), 'url')

    # Save the extracted tables (if any)
    if tables:
        file_storage.save(tables, os.path.basename(file_path), 'table')

    print(f"Extracted data saved to: {output_dir}")

if __name__ == "__main__":
    main()
