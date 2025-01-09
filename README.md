# Insurance Loss Run Processor

📄 Overview
This project processes insurance loss run reports in PDF format and transforms them into structured JSON for downstream processing and human-readable Markdown reports. It uses Python and integrates OpenAI's GPT API for text extraction and processing.

🧠 Approach and Thought Process:

1.	Requirement Analysis:
o	Extract data from PDFs into JSON and Markdown formats.
o	Handle arbitrary layouts and ensure accuracy.
o	Track OpenAI API costs and generate analytics insights.

2.	Strategic Design:
o	Modular Architecture: Clear separation into modules: Parsing, Processing, Transformation, Analytics, Cost Tracking, Output Management.
o	API Integration: Utilize OpenAI's GPT API for text extraction and processing.
o	Pipeline Flow: Each stage produces output consumed by the next stage.
o	JSON and Markdown Output: Generate structured JSON and human-readable Markdown reports.

3.	Key Design Decisions:
o	Used PyMuPDF for PDF parsing.
o	Leveraged OpenAI API for dynamic data interpretation.
o	Implemented Pandas for analytics and insights.
o	Ensured robust error handling and logging across all stages.

🚀 Features
- 📄 Extracts text and metadata from PDF reports.
- 🔄 Transforms extracted content into structured JSON and Markdown.
- 📊 Generates analytics with insights on claims.
- 💸 Tracks API costs for transparency.
- 🔧 Modular, scalable, and adaptable design.

🛠️ Setup Instructions

 1. Clone the Repository

git clone 
cd insurance_loss_run_processor


 2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  


 3. Install Dependencies

pip install -r requirements.txt


 4. Add API Key
Set your OpenAI API key in config/config.json:

 api_key=xyz 


📂 Project Structure

insurance_loss_run_processor/
├── config/              # Configuration files
├── data/                # Input and output files
│   ├── input/           # Sample PDFs
│   ├── output/          # Generated JSON, Markdown, and reports
├── src/                 # Source code modules
├── tests/               # Test scripts
├── logs/                # Logs for debugging
├── run.py               # Main entry point
├── requirements.txt     # Dependencies
└── README.md            # Documentation


⚙️ Usage

#Run the Solution

python run.py data/input/sample.pdf  

#Outputs are saved in the `data/output` directory.

🧪 Testing
Run all tests using `unittest`:

python -m unittest discover tests


📊 Extensibility

# Adapting the Solution to Handle Varying Formats, Layouts, and Content Structures

- Our solution is designed with robust modular architecture and flexibility to handle diverse report styles. Here’s how:

1.	Dynamic PDF Parsing:
o	The PDFParser module extracts raw text and layout data using PyMuPDF, ensuring it captures information regardless of document structure.
o	Flexibility in text extraction (e.g., handling multi-column layouts, tables, and irregular spacing).

2.	AI-Powered Text Processing:
o	The DataProcessor uses the OpenAI API to interpret and structure text dynamically.
o	Prompt engineering allows us to guide the AI to adapt to different report terminologies and styles.

3.	Configurable Processing Pipeline:
o	Modular design allows easy tweaking of parsing and processing rules via configuration files (config.json).
o	Adjust processing logic based on patterns detected in new layouts.

4.	Schema Validation:
o	JSON schema validation ensures the extracted data meets a consistent structure.
o	Any deviations trigger errors and allow corrective handling.

5.	Scalability with Modular Architecture:
o	Each module is independent and reusable, making it easier to update specific components without affecting the pipeline.

6.	Extensibility with New AI Models:
o	Support for integrating newer AI models or APIs as they become available.
o	Easily switch between AI providers (e.g., Anthropic, Perplexity) via configuration.

# Maintaining Accuracy Across Different Report Styles:

1.	AI-Driven Content Understanding:
o	OpenAI’s GPT-4 model is capable of understanding nuances in report structures and different terminologies.
o	The use of structured prompts ensures consistent outputs across varying layouts.

2.	Validation Layers:
o	Implement post-processing checks to validate data accuracy.
o	Schema-based validation for JSON ensures completeness and correctness.

3.	Fallback Mechanisms:
o	In case of inconsistent parsing, manual correction flags can be introduced.
o	Error logs highlight discrepancies for human validation.

4.	Incremental Refinement:
o	Feedback loops from real-world datasets can be used to fine-tune prompts and AI behavior.
o	Continuous improvement by analyzing edge cases.

5.	Error Logging and Monitoring:
o	Detailed logging allows quick identification of anomalies.
o	Alerts for repeated parsing failures guide iterative fixes.

# Architectural Choices for Robustness and Adaptability

1.	Modular Design:
o	Each module (PDFParser, DataProcessor, Transformer, etc.) operates independently.
o	Enhancements in one module do not disrupt others.

2.	Pipeline Workflow:
o	Each stage outputs clean, validated data for the next stage.
o	Easier to isolate and address errors at each stage.

3.	Config-Driven Design:
o	Configurable settings in config.json for API parameters, file paths, and parsing rules.
o	Avoids hard-coded logic, allowing dynamic adjustments.

4.	Scalable Infrastructure:
o	Capable of processing multiple documents concurrently.
o	Future-ready for deployment on cloud platforms (e.g., AWS, Azure).

5.	Monitoring and Observability:
o	Detailed logs and monitoring help track the pipeline’s performance and accuracy.
o	Alerts for anomalies ensure proactive issue resolution.

# Future Improvements
- Integrate advanced layout parsers (e.g., Tesseract OCR for scanned PDFs).
- Custom rules for extracting additional fields.
- Optimise Prompt in data_processor.
- Give more context and precise examples.
- A web interface for real-time processing.