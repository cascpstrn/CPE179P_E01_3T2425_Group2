# CPE179P_E01_3T2425_Group2

Fruit Classification with Average Calorie Counter

Overview

This project implements YOLOv8 to classify fruit. It uses FastAPI to run the server and Flet for creating client GUI.

Installation

1. Create Virtual Environment

python3 -m venv venv

source venv/bin/activate

2. Install Dependencies

pip install flet

pip install opencv-python

pip install pillow

pip install fastapi

pip install uvicorn

pip install ultralytics

3. Running the Project

Server (FastAPI)

cd server (folder where the server is located)

uvicorn server_fastapi:app --reload --host 0.0.0.0 --port 5000

Client (Flet App)

cd client (folder where the client is located)

python ui2.0.py

Dataset

We used fruit classification dataset for training and evaluation.

Architecture

FastAPI server loads YOLOv8 model and logic for average calorie content

Flet client sends video stream and displays results

Communication via REST API 

Contributors

Group02: Beltran, Cali-at, Capistrano

