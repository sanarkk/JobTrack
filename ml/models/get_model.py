import os
from huggingface_hub import hf_hub_download

def download_model():
    repo_id = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
    filename = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
    
    # Path relative to the script
    model_dir = os.path.join(os.getcwd())
    model_path = os.path.join(model_dir, filename)
        
    if not os.path.exists(model_path):
        print(f"Downloading {filename} from {repo_id}...")
        try:
            hf_hub_download(
                repo_id=repo_id, 
                filename=filename, 
                local_dir=model_dir, 
                local_dir_use_symlinks=False
            )
            print("Download complete!")
        except Exception as e:
            print(f"Error downloading model: {e}")
    else:
        print(f"Model already exists at {model_path}")

if __name__ == "__main__":
    download_model()
