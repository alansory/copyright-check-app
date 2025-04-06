# 🛡️ AI-Powered Copyright Checker (Backend)

A Flask-based backend API for detecting potential copyright infringement in images using AI models **CLIP** and **ViT** from Hugging Face.

---

## 🚀 Key Features

- 🔍 Detects potential **copyright infringement** based on visual similarity and textual context.
- 🧠 Uses a combination of:
  - `openai/clip-vit-base-patch32` for image-text similarity
  - `google/vit-base-patch16-224` for visual similarity with reference images
- 🖼️ Accepts image uploads via a simple REST API
- 🎛️ Supports `mock` (randomized) or `real` (actual AI inference) modes via `.env` configuration

---

## 📁 Project Structure

```
backend/
├── app.py                 # Main Flask application
├── reference_images/      # Folder for reference images (required for real mode)
├── uploads/               # Folder for uploaded user images
├── .env                   # Environment config (e.g., AI_MODE=real or mock)
├── requirements.txt       # All required dependencies
└── README.md              # This documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/alansory/copyright-check-app.git
   cd copyright-check-app/backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Create the `.env` file:**
   ```bash
   echo "AI_MODE=real" > .env
   ```

5. **(Optional) Add reference images to the `reference_images/` folder**

6. **Run the Flask server:**
   ```bash
   python app.py
   ```

---

## 📡 API Endpoint

### `POST /check_copyright`

**Description:** Checks whether an uploaded image is potentially copyrighted.

**Form-Data Body:**
- `image`: an image file (JPG or PNG)

**Sample Response:**
```json
{
  "file_id": "1234_sample.jpg",
  "verdict": "Copyright Infringed",
  "confidence": 94.2
}
```

---

## 🧪 Quick Test

Use `curl`:
```bash
curl -X POST http://localhost:5001/check_copyright \
  -F image=@your_image.jpg
```

Or test it via Postman or a frontend.

---

## ❓ FAQ

- **Q: Getting NumPy or Torch-related errors?**
  - A: Downgrade NumPy to a 1.x version: `pip install "numpy<2"`

- **Q: No reference images?**
  - A: Add some sample images to the `reference_images/` folder. They're used for visual similarity comparison.

- **Q: Want to test without AI models?**
  - A: Set `AI_MODE=mock` in your `.env` to return random results (no model loading needed).

---

## 📦 Dependencies

- `Flask`
- `transformers`
- `torch`
- `torchvision`
- `scikit-learn`
- `Pillow`
- `python-dotenv`

---

## ⚠️ Disclaimer

This tool provides an **AI-based early indication** of potential copyright infringement. It does **not guarantee legal accuracy**. Always consult a legal professional for copyright-related matters.

---

## 🧑‍💻 Author

Made with ❤️ by [Mohammad Sopyan]
