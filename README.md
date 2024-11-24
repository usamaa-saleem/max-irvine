
# **max-irvine**

Repo for Flux Dev. This project is built to generate images using the Flux pipeline and includes Firebase integration for uploading and retrieving generated images.

---

## **Setup Instructions**

### **1. Clone the Repository**
Clone this repository to your local machine:
```bash
git clone https://github.com/usamaa-saleem/max-irvine.git
cd max-irvine
```

---

### **2. Add the `model` Folder**
The model files are not included in this repository. To add them, clone the Flux Dev repository from Hugging Face and place it in the `model` folder at the root of the project:

1. Clone the model repository:
   ```bash
   git clone https://huggingface.co/black-forest-labs/FLUX.1-dev model
   ```

2. After cloning, the structure of your project should look like this:
   ```
   max-irvine/
   ├── __pycache__/
   ├── utils/
   ├── model/  # Cloned from Hugging Face
   │   └── (model files here)
   ├── Dockerfile
   ├── README.md
   ├── docker_commands.sh
   ├── flux-dev.png
   ├── main.py
   ├── requirements.txt
   ├── start.sh
   ```

---

### **3. Replace Firebase Credentials**
To enable Firebase integration, replace the placeholder Firebase credentials file (`utils/creds.json`) with your own Firebase service account credentials.

1. Go to the Firebase Console and generate a new service account key:
   - Navigate to **Project Settings** > **Service Accounts**.
   - Click on **Generate New Private Key** to download the JSON file.

2. Replace the existing `utils/creds.json` file with your Firebase credentials:
   ```bash
   cp /path/to/your-firebase-credentials.json utils/creds.json
   ```

---

### **4. Build the Docker Image**
After adding the `model` folder and Firebase credentials, build the Docker image.

1. Build the image:
   ```bash
   docker build -t flux-dev .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 flux-dev
   ```

---

### **5. Test the API**
Once the container is running, test the API by sending a POST request to generate an image.

#### Example Request:
```bash
curl -X POST http://127.0.0.1:8000/generate-image/ -H "Content-Type: application/json" -d '{"prompt": "A futuristic cityscape at sunset", "height": 1024, "width": 768, "num_inference_steps": 50}'
```

#### Example Response:
The response will contain a public URL for the generated image:
```json
{
    "public_url": "https://your-firebase-bucket-url/path-to-generated-image.png"
}
```

---

### **Environment Setup Checklist**
- **Clone the repository**: Ensure the repository is cloned locally.
- **Clone the model**: Use the Hugging Face repository (`https://huggingface.co/black-forest-labs/FLUX.1-dev`) for the `model` folder.
- **Add Firebase credentials**: Replace the placeholder `utils/creds.json` file with your Firebase service account JSON.

---

### **Known Issues**
1. **Large Build Context**: The `model` folder should only be added locally and not included in the Docker build context. This is managed automatically using a `.dockerignore` file.
2. **Firebase Misconfiguration**: Ensure the `creds.json` file is valid and has appropriate permissions for writing to your Firebase bucket.

---

### **Helpful Commands**

#### Build Docker Image:
```bash
docker build -t flux-dev .
```

#### Run Docker Container:
```bash
docker run -p 8000:8000 flux-dev
```

#### Test API Locally:
```bash
curl -X POST http://127.0.0.1:8000/generate-image/ -H "Content-Type: application/json" -d '{"prompt": "A futuristic cityscape at sunset", "height": 1024, "width": 768, "num_inference_steps": 50}'
```
