from pathlib import Path
from huggingface_hub import hf_hub_download

def download_model():
    repo_id = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
    filename = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
    
    # Always save next to this script (ml/models)
    model_dir = Path(__file__).resolve().parent
    model_path = model_dir / filename
        
    if not model_path.exists():
        print(f"Downloading {filename} from {repo_id}...")
        try:
            hf_hub_download(
                repo_id=repo_id, 
                filename=filename, 
                local_dir=str(model_dir), 
                local_dir_use_symlinks=False
            )
            print("Download complete!")
        except Exception as e:
            print(f"Error downloading model: {e}")
    else:
        print(f"Model already exists at {model_path}")

if __name__ == "__main__":
    download_model()
