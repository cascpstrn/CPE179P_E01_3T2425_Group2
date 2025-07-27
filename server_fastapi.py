from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import base64
import io
from PIL import Image
from ultralytics import YOLO

model = YOLO("/home/casc/Desktop/projects/179pproject/yolov8s.pt")

calorie_map = {
    "apple": 52,
    "banana": 89,
    "orange": 47,
    "grape": 69,
    "mango": 60
}


app = FastAPI()

class ImageRequest(BaseModel):
    image: str

@app.post("/predict")
async def predict(request: ImageRequest):
    try:
        image_data = base64.b64decode(request.image)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        results = model.predict(image, conf=0.25)
        boxes = results[0].boxes
        if boxes:
            class_id = int(boxes.cls[0].item())
            class_name = model.names[class_id]
            calories = calorie_map.get(class_name, "Unknown")
        else:
            class_name = "None"
            calories = "N/A"

        return {"fruit": class_name, "calories": calories}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
    #run in terminal uvicorn server_fastapi:app --reload --host 0.0.0.0 --port 5000

