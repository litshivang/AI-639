import json
import logging
import os

# Configure logging
logging.basicConfig(
    filename='logs/transformer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Transformer:
    def __init__(self, output_dir="data/output"):
        """
        Initialize Transformer with the output directory.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logging.info(f"Transformer initialized with output directory: {self.output_dir}")

    def save_json(self, data, filename="output.json"):
        """
        Save structured data as a JSON file.
        
        Args:
            data (dict): The structured JSON data.
            filename (str): Output filename.
        """
        try:
            json_path = os.path.join(self.output_dir, filename)
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logging.info(f"Saved JSON data to {json_path}")
        except Exception as e:
            logging.error(f"Failed to save JSON file: {e}")
            raise e

    def generate_markdown(self, data, filename="output.md"):
        """
        Generate a Markdown report from structured data.
        
        Args:
            data (dict): The structured JSON data.
            filename (str): Output filename.
        """
        try:
            md_path = os.path.join(self.output_dir, filename)
            with open(md_path, 'w') as md_file:
                md_file.write(f"# Insurance Loss Run Report\n\n")
                md_file.write(f"**Policy Number:** {data.get('policy_number', 'N/A')}\n")
                md_file.write(f"**Insured Name:** {data.get('insured_name', 'N/A')}\n\n")
                md_file.write("## Losses:\n")
                for loss in data.get('losses', []):
                    md_file.write(f"- **Claim Number:** {loss.get('claim_number', 'N/A')}\n")
                    md_file.write(f"  - **Date of Loss:** {loss.get('date_of_loss', 'N/A')}\n")
                    md_file.write(f"  - **Amount:** {loss.get('amount', 'N/A')}\n")
                    md_file.write(f"  - **Description:** {loss.get('description', 'N/A')}\n\n")
            logging.info(f"Saved Markdown report to {md_path}")
        except Exception as e:
            logging.error(f"Failed to generate Markdown file: {e}")
            raise e

    def transform(self, data):
        """
        Transform data into both JSON and Markdown formats.
        
        Args:
            data (dict): The structured JSON data.
        """
        try:
            self.save_json(data)
            self.generate_markdown(data)
            logging.info("Data transformation completed successfully.")
        except Exception as e:
            logging.error(f"Failed to transform data: {e}")
            raise e


# Example usage
if __name__ == "__main__":
    sample_data = {
        "policy_number": "12345",
        "insured_name": "John Doe",
        "losses": [
            {
                "claim_number": "ABC123",
                "date_of_loss": "2024-01-01",
                "amount": "$1000",
                "description": "Minor accident"
            }
        ]
    }

    transformer = Transformer()
    transformer.transform(sample_data)
