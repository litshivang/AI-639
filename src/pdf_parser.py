import fitz  # PyMuPDF
import logging
import os

# Configure logging
logging.basicConfig(
    filename='logs/pdf_parser.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PDFParser:
    def __init__(self, pdf_path):
        """
        Initialize PDFParser with the path to the PDF file.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")
        self.pdf_path = pdf_path
        logging.info(f"PDFParser initialized for file: {pdf_path}")

    def extract_text(self):
        """
        Extract text content from the PDF file.
        Returns:
            str: The extracted text from the PDF.
        """
        text_content = ""
        try:
            with fitz.open(self.pdf_path) as pdf_document:
                for page_num in range(len(pdf_document)):
                    page = pdf_document[page_num]
                    text_content += page.get_text()
            logging.info(f"Extracted text from {self.pdf_path}")
        except Exception as e:
            logging.error(f"Failed to extract text: {e}")
            raise e
        return text_content

    def extract_metadata(self):
        """
        Extract metadata from the PDF file.
        Returns:
            dict: Metadata dictionary.
        """
        try:
            with fitz.open(self.pdf_path) as pdf_document:
                metadata = pdf_document.metadata
            logging.info(f"Extracted metadata from {self.pdf_path}")
            return metadata
        except Exception as e:
            logging.error(f"Failed to extract metadata: {e}")
            raise e

    def parse_pdf(self):
        """
        Parse the PDF to extract text and metadata.
        Returns:
            dict: Dictionary containing text and metadata.
        """
        try:
            text = self.extract_text()
            metadata = self.extract_metadata()
            result = {
                "metadata": metadata,
                "text": text
            }
            logging.info(f"Successfully parsed {self.pdf_path}")
            return result
        except Exception as e:
            logging.error(f"Failed to parse PDF: {e}")
            raise e


# Example usage
if __name__ == "__main__":
    parser = PDFParser("data/input/sample.pdf")
    result = parser.parse_pdf()
    print(result)
