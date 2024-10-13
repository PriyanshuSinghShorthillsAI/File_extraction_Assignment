import os
from PyPDF2 import PdfReader
from loaders.file_loader import FileLoader

class PDFLoader(FileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.file = None

    def validate_file(self):
        if not os.path.exists(self.file_path):
            raise ValueError(f"File not found: {self.file_path}")
        if not self.file_path.lower().endswith(".pdf"):
            raise ValueError(f"Invalid file type: {self.file_path} is not a PDF file.")

    def load_file(self):
        try:
            self.file = open(self.file_path, "rb")
            return PdfReader(self.file)
        except Exception as e:
            raise ValueError(f"Error loading PDF file: {e}")

    def close_file(self):
        if self.file:
            self.file.close()
