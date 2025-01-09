import argparse
import logging
from src.pdf_parser import PDFParser
from src.data_processor import DataProcessor
from src.transformer import Transformer
from src.analytics import Analytics
from src.cost_tracker import CostTracker
from src.output_manager import OutputManager

# Configure logging
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main(pdf_path):
    try:
        logging.info("Starting the PDF processing pipeline.")
        
        # Step 1: PDF Parsing
        parser = PDFParser(pdf_path)
        pdf_data = parser.parse_pdf()
        text_content = pdf_data['text']
        metadata = pdf_data['metadata']
        
        # Step 2: Data Processing (OpenAI API)
        processor = DataProcessor()
        structured_data = processor.process_text(text_content)
        api_usage = {"prompt_tokens": 500, "completion_tokens": 1500, "total_tokens": 2000}  # Replace with real usage data
        
        # Step 3: Data Transformation
        transformer = Transformer()
        transformer.transform(structured_data)
        
        # Step 4: Analytics (Optional)
        analytics = Analytics("data/output/output.json")
        analytics.run()
        
        # Step 5: Cost Tracking
        cost_tracker = CostTracker()
        cost_tracker.run(api_usage)
        
        # Step 6: Output Management
        output_manager = OutputManager()
        output_manager.save_file(
            content="Processing completed successfully.",
            file_type="markdown",
            file_name_prefix="pipeline_summary"
        )
        
        logging.info("PDF processing pipeline completed successfully.")
        print("✅ Pipeline executed successfully. Check the 'data/output' directory for results.")
    
    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}")
        print(f"❌ Pipeline execution failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insurance Loss Run Report Processor")
    parser.add_argument("pdf_path", help="Path to the PDF file to process")
    args = parser.parse_args()
    
    main(args.pdf_path)

