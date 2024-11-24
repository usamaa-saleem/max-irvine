from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import torch
from diffusers import FluxPipeline
from firebase_admin import credentials, initialize_app, storage
import uuid

# Initialize Firebase
cred = credentials.Certificate("utils/creds.json")  # Replace with your Firebase credentials file
initialize_app(cred, {'storageBucket': 'imagegen-54a5f.appspot.com'})  # Replace with your bucket name

# Initialize FastAPI
app = FastAPI()

# Load model locally
MODEL_PATH = "model/FLUX.1-dev"  # Path to the local model
pipe = FluxPipeline.from_pretrained(MODEL_PATH, torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()  # Remove if enough GPU VRAM is available

# API Request Schema
class GenerateImageRequest(BaseModel):
    prompt: str
    height: int = 1024  # Default value if not provided
    width: int = 1024   # Default value if not provided
    num_inference_steps: int = 50  # Default value if not provided

# Helper function to upload to Firebase
def upload_to_firebase(local_path: str) -> str:
    bucket = storage.bucket()
    unique_name = f"generated-images/{uuid.uuid4()}.png"
    blob = bucket.blob(unique_name)
    blob.upload_from_filename(local_path)
    blob.make_public()
    return blob.public_url

# API Endpoint for generating images
@app.post("/generate-image/")
async def generate_image(request: GenerateImageRequest):
    try:
        prompt = request.prompt
        height = request.height
        width = request.width
        num_inference_steps = request.num_inference_steps
        output_path = "output_image.png"

        # Generate the image
        image = pipe(
            prompt,
            height=height,
            width=width,
            guidance_scale=3.5,
            num_inference_steps=num_inference_steps,
            max_sequence_length=512,
            generator=torch.Generator("cpu").manual_seed(0),
        ).images[0]
        image.save(output_path)

        # Upload to Firebase
        public_url = upload_to_firebase(output_path)

        # Remove the local file
        os.remove(output_path)

        return JSONResponse(content={"public_url": public_url})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))