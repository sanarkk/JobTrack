import os
from pathlib import Path
from llama_cpp import Llama
from ml.models.get_model import download_model

# Global variable for Singleton Pattern
LLM_MODEL = None
MODEL_DIR = Path(__file__).resolve().parents[1] / "models"
MODEL_FILENAME = "qwen2.5-1.5b-instruct-q4_k_m.gguf"


class BaseAgent:
    def __init__(self):
        """
        Base Agent that manages the connection to the Local LLM.
        Uses Singleton pattern to avoid re-loading the model for every agent.
        """
        self.model = self._get_llm_model()

    def _get_llm_model(self):
        global LLM_MODEL
        if LLM_MODEL is None:
            try:
                model_path = MODEL_DIR / MODEL_FILENAME
                if not model_path.exists():
                    print(f"Model gguf does not exist - Loading model from WEB")
                    download_model()

                print(f"Spinning up Base AI Model: {model_path.name}...")
                
                # Load Model
                LLM_MODEL = Llama(
                    model_path=str(model_path),
                    n_ctx=4096,
                    n_gpu_layers=-1,   # all layers to GPU
                    n_threads=10,
                    n_batch=512,
                )
                
                print("Base AI Model Loaded Successfully")
            except Exception as e:
                print(f"Error loading Base AI Model: {e}")
                return None
        return LLM_MODEL

    def inference(self, system_prompt, user_prompt, max_tokens=1000, response_format=None, temperature=0.7):
        """
        Common method to generate a response from the LLM.
        """
        if not self.model:
            return None

        try:
            kwargs = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if response_format:
                kwargs["response_format"] = response_format

            response = self.model.create_chat_completion(**kwargs)
            content = response['choices'][0]['message']['content']
            
            if response_format and response_format.get("type") == "json_object":
                return self._clean_json_response(content)
                
            return content
        except Exception as e:
            print(f"Agent Inference Error: {e}")
            return None

    def _clean_json_response(self, content):
        """
        Helper to strip markdown code blocks (```json ... ```) from the response.
        """
        clean_content = content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content[7:]
        if clean_content.startswith("```"):
            clean_content = clean_content[3:]
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3]
        return clean_content.strip()
