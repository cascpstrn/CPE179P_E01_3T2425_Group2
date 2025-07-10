import flet as ft
import cv2
import threading
from PIL import Image
import io
import base64

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
    page.title = "Centered Camera Feed"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    image = ft.Image(width=640, height=480)

    # Center the image in the app
    page.add(
        ft.Column(
            [image],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

    def stream():
        for frame in get_frame():
            image.src_base64 = frame
            page.update()

    threading.Thread(target=stream, daemon=True).start()

ft.app(target=main)
