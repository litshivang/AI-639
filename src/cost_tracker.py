import json
import logging
import os

# Configure logging
logging.basicConfig(
    filename='logs/cost_tracker.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CostTracker:
    def __init__(self, output_dir="data/output"):
        """
        Initialize CostTracker with output directory.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logging.info(f"CostTracker initialized with output directory: {self.output_dir}")

    def calculate_cost(self, usage):
        """
        Calculate API cost based on token usage.
        
        Args:
            usage (dict): Token usage data from OpenAI API response.
        
        Returns:
            dict: Cost details including token breakdown and total cost.
        """
        try:
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', 0)
            
            # Example pricing per 1k tokens
            prompt_cost_per_1k = 0.03  # Adjust based on actual pricing
            completion_cost_per_1k = 0.06
            
            prompt_cost = (prompt_tokens / 1000) * prompt_cost_per_1k
            completion_cost = (completion_tokens / 1000) * completion_cost_per_1k
            total_cost = prompt_cost + completion_cost
            
            cost_data = {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "prompt_cost": round(prompt_cost, 4),
                "completion_cost": round(completion_cost, 4),
                "total_cost": round(total_cost, 4)
            }
            
            logging.info("API cost calculated successfully.")
            return cost_data
        except Exception as e:
            logging.error(f"Failed to calculate API cost: {e}")
            raise e

    def save_cost_report(self, cost_data):
        """
        Save API cost details in JSON and Markdown formats.
        
        Args:
            cost_data (dict): Calculated cost data.
        """
        try:
            json_path = os.path.join(self.output_dir, "api_cost_report.json")
            with open(json_path, 'w') as file:
                json.dump(cost_data, file, indent=4)
            logging.info(f"API cost data saved in JSON at {json_path}")

            md_path = os.path.join(self.output_dir, "api_cost_report.md")
            with open(md_path, 'w') as file:
                file.write("# API Cost Report\n\n")
                file.write(f"**Prompt Tokens:** {cost_data['prompt_tokens']}\n")
                file.write(f"**Completion Tokens:** {cost_data['completion_tokens']}\n")
                file.write(f"**Total Tokens:** {cost_data['total_tokens']}\n")
                file.write(f"**Prompt Cost:** ${cost_data['prompt_cost']:.4f}\n")
                file.write(f"**Completion Cost:** ${cost_data['completion_cost']:.4f}\n")
                file.write(f"**Total Cost:** ${cost_data['total_cost']:.4f}\n")
            logging.info(f"API cost data saved in Markdown at {md_path}")
        except Exception as e:
            logging.error(f"Failed to save API cost report: {e}")
            raise e

    def run(self, usage):
        """
        Execute the cost tracking pipeline.
        
        Args:
            usage (dict): Token usage data from OpenAI API response.
        """
        try:
            cost_data = self.calculate_cost(usage)
            self.save_cost_report(cost_data)
            logging.info("Cost tracking pipeline executed successfully.")
        except Exception as e:
            logging.error(f"Cost tracking pipeline failed: {e}")
            raise e


# Example usage
if __name__ == "__main__":
    usage_data = {
        "prompt_tokens": 500,
        "completion_tokens": 1500,
        "total_tokens": 2000
    }
    
    tracker = CostTracker()
    tracker.run(usage_data)
