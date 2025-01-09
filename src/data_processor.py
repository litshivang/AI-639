import openai
import logging
import json
import os
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    filename='logs/data_processor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataProcessor:
    def __init__(self):
        """
        Initialize the DataProcessor with configuration from JSON file.
        """
        try:
            config_path = 'config/config.json'
            with open(config_path, 'r') as f:
                config = json.load(f)
            openai.api_key = config.get('api_key')
            
            if not openai.api_key:
                raise ValueError("OpenAI API key is not set.")
            
            # Load additional configuration
            self.chunk_size = config.get('chunk_size', 1500)
            self.max_tokens = config.get('max_tokens', 1500)
            self.temperature = config.get('temperature', 0.2)
            self.model = config.get('model', 'gpt-4')
            
            logging.info("DataProcessor initialized successfully with configurations.")
        except Exception as e:
            logging.error(f"Initialization failed: {str(e)}")
            raise

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into manageable chunks while preserving context.
        """
        chunks = []
        start = 0
        while start < len(text):
            # Find a good breaking point
            end = start + self.chunk_size
            if end < len(text):
                # Try to break at a newline
                next_newline = text.find('\n', end - 100, end + 100)
                if next_newline != -1:
                    end = next_newline
            
            chunks.append(text[start:end])
            start = end
            
        return chunks

    def create_prompt(self, chunk: str) -> str:
        """
        Create a structured prompt for the OpenAI API.
        """
        return (
            "You are an AI assistant specialized in analyzing insurance loss run reports. "
            "Extract and structure the data into JSON format as specified:\n"
            "{\n"
            "  \"policy_number\": \"\",\n"
            "  \"insured_name\": \"\",\n"
            "  \"losses\": [\n"
            "    {\n"
            "      \"claim_number\": \"\",\n"
            "      \"date_of_loss\": \"\",\n"
            "      \"amount\": \"\",\n"
            "      \"description\": \"\"\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "Text:\n"
            f"{chunk}"
        )

    def _attempt_json_repair(self, text: str) -> Optional[Dict]:
        """
        Enhanced JSON repair functionality for handling various edge cases.
        """
        try:
            # Initial cleanup
            text = text.strip()
            
            # Find the main JSON object(s)
            start = text.find("{")
            end = text.rfind("}") + 1
            if start == -1 or end == 0:
                return None
            
            json_candidate = text[start:end]
            
            # Handle multiple JSON objects
            if json_candidate.count('{') > json_candidate.count('}'):
                # Find proper ending of first complete object
                depth = 0
                for i, char in enumerate(json_candidate):
                    if char == '{':
                        depth += 1
                    elif char == '}':
                        depth -= 1
                        if depth == 0:
                            json_candidate = json_candidate[:i+1]
                            break
            
            # Remove trailing commas before closing braces
            json_candidate = json_candidate.replace(',}', '}').replace(',]', ']')
            
            # Try parsing the cleaned text
            return json.loads(json_candidate)
            
        except json.JSONDecodeError as e:
            logging.error(f"JSON repair failed: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in JSON repair: {str(e)}")
            return None

    def merge_chunks(self, chunks_data: List[Dict]) -> Dict:
        """
        Merge multiple chunks into a single coherent response.
        """
        merged = {
            "policy_number": "",
            "insured_name": "",
            "losses": []
        }
        
        seen_claims = set()  # Track duplicate claims
        
        for chunk in chunks_data:
            if chunk.get("policy_number") and not merged["policy_number"]:
                merged["policy_number"] = chunk["policy_number"]
            if chunk.get("insured_name") and not merged["insured_name"]:
                merged["insured_name"] = chunk["insured_name"]
                
            # Add non-duplicate losses
            for loss in chunk.get("losses", []):
                claim_number = loss.get("claim_number", "")
                if claim_number and claim_number not in seen_claims:
                    seen_claims.add(claim_number)
                    merged["losses"].append(loss)
        
        return merged

    def process_text(self, text: str) -> Dict[str, Any]:
        """
        Process raw text using OpenAI API with enhanced error handling and chunking.
        """
        try:
            chunks = self.chunk_text(text)
            processed_chunks = []
            
            for idx, chunk in enumerate(chunks):
                logging.info(f"Processing chunk {idx + 1}/{len(chunks)} with OpenAI API.")
                
                try:
                    # Update the prompt to be more explicit about requiring JSON
                    prompt = self.create_prompt(chunk)
                    prompt += "\nIMPORTANT: Return ONLY valid JSON data. If there's not enough information, return an empty JSON structure."
                    
                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": "You are an insurance loss report processor that must always return valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=self.max_tokens,
                        temperature=self.temperature
                    )
                    
                    raw_result = response['choices'][0]['message']['content']
                    logging.info(f"Raw response for chunk {idx + 1}: {raw_result}")
                    
                    # Handle non-JSON responses
                    if not raw_result.strip().startswith('{'):
                        logging.warning(f"Chunk {idx + 1} returned non-JSON response, using empty structure")
                        chunk_data = {
                            "policy_number": "",
                            "insured_name": "",
                            "losses": []
                        }
                    else:
                        chunk_data = self._attempt_json_repair(raw_result)
                    
                    if chunk_data:
                        processed_chunks.append(chunk_data)
                        self.calculate_api_cost(response)
                    else:
                        logging.error(f"Chunk {idx + 1} processing failed: Invalid JSON")
                        continue
                        
                except Exception as e:
                    logging.error(f"Error processing chunk {idx + 1}: {str(e)}")
                    continue
                
            if not processed_chunks:
                raise ValueError("No chunks were successfully processed")
                
            # Merge all processed chunks
            return self.merge_chunks(processed_chunks)
            
        except Exception as e:
            logging.error(f"Failed to process text with OpenAI API: {str(e)}")
            raise

    def calculate_api_cost(self, response: Dict) -> float:
        """
        Calculate API cost based on token usage with updated pricing.
        """
        try:
            usage = response.get('usage', {})
            total_tokens = usage.get('total_tokens', 0)
            
            # Updated pricing for GPT-4
            cost_per_1k_tokens = 0.03 if self.model == 'gpt-3.5-turbo' else 0.06
            total_cost = (total_tokens / 1000) * cost_per_1k_tokens
            
            logging.info(f"API cost for chunk: ${total_cost:.4f} ({total_tokens} tokens)")
            return total_cost
            
        except Exception as e:
            logging.error(f"Failed to calculate API cost: {str(e)}")
            return 0.0