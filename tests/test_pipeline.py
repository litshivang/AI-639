import unittest
from src.pdf_parser import PDFParser
from src.data_processor import DataProcessor
from src.transformer import Transformer
from src.analytics import Analytics
from src.cost_tracker import CostTracker
from src.output_manager import OutputManager
import os

class TestPipeline(unittest.TestCase):
    
    def setUp(self):
        """
        Setup test environment.
        """
        self.sample_pdf = "data/input/sample.pdf"
        self.output_dir = "data/output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def test_pdf_parser(self):
        """
        Test PDF Parsing Module.
        """
        parser = PDFParser(self.sample_pdf)
        result = parser.parse_pdf()
        self.assertIn('text', result)
        self.assertIn('metadata', result)
    
    def test_data_processor(self):
        """
        Test Data Processing Module.
        """
        sample_text = "Policy: LTCM-789234-02\nInsured: John Doe"
        processor = DataProcessor()
        result = processor.process_text(sample_text)
        self.assertIn('Policy', result)
        self.assertIn('insured_name', result)
    
    def test_transformer(self):
        """
        Test Data Transformation Module.
        """
        transformer = Transformer(self.output_dir)
        sample_data = {
            "Policy": "LTCM-789234-02",
            "insured": "John Doe",
            "losses": [{"claim_number": "ABC123", "amount": "$1000"}]
        }
        transformer.transform(sample_data)
        self.assertTrue(os.path.exists(f"{self.output_dir}/output.json"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/output.md"))
    
    def test_analytics(self):
        """
        Test Analytics Module.
        """
        analytics = Analytics(f"{self.output_dir}/output.json")
        analytics.run()
        self.assertTrue(os.path.exists(f"{self.output_dir}/analytics_summary.json"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/analytics_summary.md"))
    
    def test_cost_tracker(self):
        """
        Test Cost Tracking Module.
        """
        cost_tracker = CostTracker(self.output_dir)
        sample_usage = {"prompt_tokens": 1000, "completion_tokens": 2000, "total_tokens": 3000}
        cost_tracker.run(sample_usage)
        self.assertTrue(os.path.exists(f"{self.output_dir}/api_cost_report.json"))
        self.assertTrue(os.path.exists(f"{self.output_dir}/api_cost_report.md"))
    
    def test_output_manager(self):
        """
        Test Output Management Module.
        """
        manager = OutputManager(self.output_dir)
        file_path = manager.save_file("Test content", "markdown", "test_output")
        self.assertTrue(os.path.exists(file_path))
    
    def tearDown(self):
        """
        Cleanup test environment.
        """
        pass


if __name__ == '__main__':
    unittest.main()
