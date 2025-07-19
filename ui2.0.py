import flet as ft
import cv2
import threading
from PIL import Image
import io
import base64
import requests

# URL of the locally running model server
JETSON_URL = "http://127.0.0.1:5000/predict"

def get_frame():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((640, 480))
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_data = buffer.getvalue()
        buffer.close()
        img_base64 = base64.b64encode(img_data).decode("utf-8")
        yield img_base64
    cap.release()

def main(page: ft.Page):
    page.title = "Fruit Identifier with Calorie Counter"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    image = ft.Image(width=640, height=480)
    result_text = ft.Text(value="Identifying...", size=20, weight="bold")

    # Layout: Camera feed + prediction text
    page.add(
        ft.Column(
            [image, result_text],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    def stream():
        for frame in get_frame():
            image.src_base64 = frame
            page.update()

            try:
                # Send frame to the model server
                response = requests.post(JETSON_URL, json={"image": frame})
                if response.status_code == 200:
                    result = response.json()
                    fruit = result.get("fruit", "Unknown")
                    calories = result.get("calories", "N/A")
                    result_text.value = f"Fruit: {fruit} | Calories: {calories}"
                else:
                    result_text.value = "Prediction failed"
            except Exception as e:
                result_text.value = f"Error: {str(e)}"
            
            page.update()

    threading.Thread(target=stream, daemon=True).start()

ft.app(target=main)
