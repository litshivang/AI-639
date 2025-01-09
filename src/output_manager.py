import os
import shutil
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='logs/output_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class OutputManager:
    def __init__(self, base_dir="data/output"):
        """
        Initialize OutputManager with the base directory for outputs.
        """
        self.base_dir = base_dir
        self.json_dir = os.path.join(base_dir, "json")
        self.markdown_dir = os.path.join(base_dir, "markdown")
        self.cost_dir = os.path.join(base_dir, "cost")
        self._create_directories()
        logging.info(f"OutputManager initialized with base directory: {self.base_dir}")

    def _create_directories(self):
        """
        Create necessary output directories if they do not exist.
        """
        for directory in [self.json_dir, self.markdown_dir, self.cost_dir]:
            os.makedirs(directory, exist_ok=True)
            logging.info(f"Directory ensured: {directory}")

    def save_file(self, content, file_type, file_name_prefix):
        """
        Save content to the appropriate directory based on file type.
        
        Args:
            content (str): The content to save.
            file_type (str): Type of file ('json', 'markdown', 'cost').
            file_name_prefix (str): Prefix for the file name.
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_extension = {
                'json': '.json',
                'markdown': '.md',
                'cost': '.json'
            }.get(file_type, '.txt')

            directory = {
                'json': self.json_dir,
                'markdown': self.markdown_dir,
                'cost': self.cost_dir
            }.get(file_type, self.base_dir)

            file_name = f"{file_name_prefix}_{timestamp}{file_extension}"
            file_path = os.path.join(directory, file_name)

            with open(file_path, 'w') as file:
                file.write(content)

            logging.info(f"Saved {file_type} file at {file_path}")
            return file_path
        except Exception as e:
            logging.error(f"Failed to save {file_type} file: {e}")
            raise e

    def clean_old_outputs(self, days=7):
        """
        Clean output files older than a specified number of days.
        
        Args:
            days (int): Number of days after which files are considered old.
        """
        try:
            now = datetime.now()
            for directory in [self.json_dir, self.markdown_dir, self.cost_dir]:
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        file_age = (now - datetime.fromtimestamp(os.path.getmtime(file_path))).days
                        if file_age > days:
                            os.remove(file_path)
                            logging.info(f"Deleted old file: {file_path}")
        except Exception as e:
            logging.error(f"Failed to clean old outputs: {e}")
            raise e

    def list_outputs(self, file_type):
        """
        List all files of a specific type.
        
        Args:
            file_type (str): Type of files to list ('json', 'markdown', 'cost').
        
        Returns:
            list: List of file paths.
        """
        try:
            directory = {
                'json': self.json_dir,
                'markdown': self.markdown_dir,
                'cost': self.cost_dir
            }.get(file_type, self.base_dir)

            files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            logging.info(f"Listed {file_type} outputs: {files}")
            return files
        except Exception as e:
            logging.error(f"Failed to list {file_type} outputs: {e}")
            raise e


# Example usage
if __name__ == "__main__":
    manager = OutputManager()
    
    # Example JSON output
    json_content = '{"policy_number": "12345", "insured_name": "John Doe"}'
    manager.save_file(json_content, 'json', 'policy_data')
    
    # Example Markdown output
    md_content = "# Policy Report\n**Policy Number:** 12345\n**Insured Name:** John Doe"
    manager.save_file(md_content, 'markdown', 'policy_report')
    
    # Example Cost output
    cost_content = '{"total_cost": 1.23}'
    manager.save_file(cost_content, 'cost', 'api_cost')
    
    # List files
    print(manager.list_outputs('json'))
    
    # Clean old outputs
    manager.clean_old_outputs(days=7)
