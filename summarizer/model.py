import torch
from transformers import pipeline

class ModelLoader:
    _pipeline = None

    @classmethod
    def get_pipeline(cls):
        if cls._pipeline is None:
            print("⏳ Loading Qwen2.5-1.5B Model... (First run only)")
            # Qwen2.5-1.5B-Instruct is the sweet spot for CPU speed vs intelligence
            cls._pipeline = pipeline(
                "text-generation",
                model="Qwen/Qwen2.5-1.5B-Instruct",
                device=-1,  # -1 means CPU
                dtype=torch.float32, 
                trust_remote_code=True
            )
        return cls._pipeline