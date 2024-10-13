import unittest
from loaders.pdf_loader import PDFLoader
from extractors.data_extractor import DataExtractor

class TestExtractor(unittest.TestCase):
    def test_pdf_extraction(self):
        loader = PDFLoader('sample.pdf')
        extractor = DataExtractor(loader)
        text_data = extractor.extract_text()
        self.assertTrue(len(text_data) > 0)

if __name__ == '__main__':
    unittest.main()
