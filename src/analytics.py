import pandas as pd
import logging
import json
from typing import Dict, Any, Optional
import os

class Analytics:
    def __init__(self, data_file: str):
        """Initialize Analytics with data file path."""
        self.data_file = data_file
        logging.info(f"Analytics initialized with data file: {data_file}")

    def load_data(self) -> pd.DataFrame:
        """Load and preprocess data from JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Flatten the JSON structure
            flattened_data = []
            for loss in data.get('losses', []):
                loss_data = {
                    'policy_number': data.get('policy_number', ''),
                    'insured_name': data.get('insured_name', ''),
                    **loss
                }
                flattened_data.append(loss_data)
            
            df = pd.DataFrame(flattened_data)
            logging.info("Loaded data into Pandas DataFrame.")
            return df
            
        except Exception as e:
            logging.error(f"Failed to load data: {str(e)}")
            raise

    def clean_amount(self, amount: str) -> float:
        """Clean and convert amount strings to float values."""
        try:
            if not amount or pd.isna(amount):
                return 0.0
            # Remove currency symbols and commas, then convert to float
            cleaned = amount.replace('$', '').replace(',', '').strip()
            return float(cleaned) if cleaned else 0.0
        except (ValueError, AttributeError):
            logging.warning(f"Could not convert amount '{amount}' to float, using 0.0")
            return 0.0

    def generate_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate analytics summary with proper data type handling."""
        try:
            # Convert amount column to numeric values
            df['amount_numeric'] = df['amount'].apply(self.clean_amount)
            
            summary = {
                'total_claims': len(df),
                'total_amount': df['amount_numeric'].sum(),
                'average_amount': df['amount_numeric'].mean(),
                'max_amount': df['amount_numeric'].max(),
                'min_amount': df['amount_numeric'].min(),
                'zero_amount_claims': len(df[df['amount_numeric'] == 0]),
                'unique_drivers': len(df['description'].unique()),
                'claims_by_month': df['date_of_loss'].value_counts().to_dict()
            }
            
            logging.info("Generated analytics summary successfully")
            return summary
            
        except Exception as e:
            logging.error(f"Failed to generate analytics summary: {str(e)}")
            raise
    def save_summary(self, summary):
            """
            Save analytics summary in JSON and Markdown formats.
            """
            try:
                summary_path = os.path.join(self.output_dir, "analytics_summary.json")
                with open(summary_path, 'w') as file:
                    json.dump(summary, file, indent=4)
                logging.info(f"Saved analytics summary to {summary_path}")

                md_path = os.path.join(self.output_dir, "analytics_summary.md")
                with open(md_path, 'w') as file:
                    file.write("# Analytics Summary\n\n")
                    file.write(f"**Total Claims:** {summary['total_claims']}\n")
                    file.write(f"**Total Loss Amount:** ${summary['total_loss_amount']:.2f}\n")
                    file.write(f"**Average Loss Amount:** ${summary['average_loss_amount']:.2f}\n")
                    file.write(f"**Most Recent Claim Date:** {summary['most_recent_claim_date']}\n")
                logging.info(f"Saved analytics summary in Markdown format at {md_path}")
            except Exception as e:
                logging.error(f"Failed to save analytics summary: {e}")
                raise e
    def run(self) -> Optional[Dict[str, Any]]:
        """Run the analytics pipeline with error handling."""
        try:
            df = self.load_data()
            summary = self.generate_summary(df)
            logging.info("Analytics pipeline completed successfully")
            return summary
            
        except Exception as e:
            logging.error(f"Analytics pipeline failed: {str(e)}")
            return None