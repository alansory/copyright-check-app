
# 📷 Copyright Check App (Frontend)

A simple Vue.js frontend application that allows users to upload an image, preview it, and check if the image is copyrighted via backend API integration.

---

## 🚀 Features

- Upload images via click or drag-and-drop
- Preview uploaded image
- Submit image to backend for copyright check
- Reset/clear uploaded image and result
- Responsive, clean, and accessible UI using Tailwind CSS

---

## 🧱 Tech Stack

- [Vue 3](https://vuejs.org/) (Composition API)
- [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- Pinia (state management)

---

## 🔧 Setup & Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/copyright-check-app
   cd copyright-check-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run in development mode:**
   ```bash
   npm run dev
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

---

## 🌐 API Integration

The frontend is designed to send a `POST` request to a backend endpoint for copyright checking:

- **Endpoint:** `POST /api/check-copyright`
- **Payload:** `FormData` with image file
- **Response format:**
  ```json
  {
    "file_id": "1234_sample.jpg",
    "verdict": "Copyright Infringed",
    "confidence": 94.2
  }
  ```

You can update the API base URL in your environment or configuration file.

---

## 🧑‍💻 Author

Made with ❤️ by [Mohammad Sopyan]
