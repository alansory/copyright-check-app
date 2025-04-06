from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
from dotenv import load_dotenv
from transformers import CLIPProcessor, CLIPModel, ViTModel, ViTFeatureExtractor
from PIL import Image
import torch
from torchvision import transforms
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)
CORS(app)

load_dotenv()
AI_MODE = os.getenv("AI_MODE", "mock")

# Load models if using real AI
if AI_MODE == "real":
    # CLIP
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
    # ViT
    vit_model = ViTModel.from_pretrained("google/vit-base-patch16-224")
    vit_feature_extractor = ViTFeatureExtractor.from_pretrained("google/vit-base-patch16-224")

# Image transformation for ViT
vit_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Get ViT embedding
def get_vit_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = vit_feature_extractor(images=image, return_tensors="pt")
    outputs = vit_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].detach().numpy()

# Compare to all reference images
def check_visual_similarity(user_image_path, threshold=0.9):
    user_embedding = get_vit_embedding(user_image_path)
    reference_dir = "reference_images"
    max_sim = 0.0

    for fname in os.listdir(reference_dir):
        ref_path = os.path.join(reference_dir, fname)
        ref_embedding = get_vit_embedding(ref_path)
        sim = cosine_similarity(user_embedding, ref_embedding)[0][0]
        max_sim = max(max_sim, sim)

    return max_sim

# Real AI copyright check
def real_copyright_check(file_path):
    # === CLIP TEXT MATCHING ===
    image = Image.open(file_path).convert("RGB")
    reference_texts = ["This image is copyrighted material", "This image is free to use"]
    inputs = clip_processor(text=reference_texts, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1).detach().numpy()[0]

    clip_verdict = "Copyright Infringed" if probs[0] > probs[1] else "No Issue"
    clip_conf = round(max(probs) * 100, 1)

    # === ViT SIMILARITY CHECK ===
    max_sim = check_visual_similarity(file_path)
    vit_verdict = "Copyright Infringed" if max_sim >= 0.9 else "No Issue"

    # Combine verdicts
    if clip_verdict == "Copyright Infringed" or vit_verdict == "Copyright Infringed":
        final_verdict = "Copyright Infringed"
        final_confidence = max(clip_conf, round(max_sim * 100, 1))
    else:
        final_verdict = "No Issue"
        final_confidence = min(clip_conf, round((1 - max_sim) * 100, 1))

    return final_verdict, final_confidence

# Mock fallback
def mock_copyright_check(file_path):
    verdict = random.choice(["Copyright Infringed", "No Issue"])
    confidence = round(random.uniform(50.0, 99.9), 1)
    return verdict, confidence

copyright_check = real_copyright_check if AI_MODE == "real" else mock_copyright_check

@app.route('/check_copyright', methods=['POST'])
def check_copyright():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']
    file_id = f"{random.randint(1000, 9999)}_{image.filename}"
    file_path = os.path.join("uploads", file_id)
    os.makedirs("uploads", exist_ok=True)
    image.save(file_path)

    verdict, confidence = copyright_check(file_path)

    return jsonify({
        "file_id": file_id,
        "verdict": verdict,
        "confidence": confidence
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
