import docx
from loaders.file_loader import FileLoader

class DOCXLoader(FileLoader):
    def validate_file(self):
        if not self.file_path.endswith('.docx'):
            raise ValueError("Invalid file type. Expected a DOCX file.")

    def load_file(self):
        return docx.Document(self.file_path)