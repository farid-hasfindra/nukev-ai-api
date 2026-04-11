import uvicorn
from app.main import app

# Entry point khusus untuk HuggingFace Spaces atau deployment cloud lainnya
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=7860, reload=False)
