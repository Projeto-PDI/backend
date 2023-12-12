from collections import defaultdict
from datetime import datetime
import cv2
import numpy as np
import math
import json
from json import JSONEncoder
from io import BytesIO
import tempfile
import logging
from ultralytics import YOLO

logging.getLogger("opencv-python").setLevel(logging.ERROR)

class DateTimeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


class TrajectoryVelocityProcessing:
    def __init__(self, model_path="yolov8n.pt"):
        # Load the YOLOv8 model
        self.model = YOLO("yolov8n.pt")

        # Store the track history
        self.track_history = defaultdict(lambda: [])
        self.speed_history = defaultdict(lambda: [])
        self.start_time = defaultdict(lambda: [])
        self.end_time = defaultdict(lambda: [])
        self.classes_history = defaultdict(lambda: [])

    def estimatespeed(self, Location1, Location2):
        # Euclidean Distance Formula
        d_pixel = math.sqrt(
            math.pow(Location2[0] - Location1[0], 2)
            + math.pow(Location2[1] - Location1[1], 2)
        )
        # definindo os pixels por metro
        print(Location1[1] / 680)
        ppm = 6 + 6 / math.sqrt(math.pow(Location1[1] / 680, 2))
        d_meters = d_pixel / (ppm)
        time_constant = 15 * 3.6
        # distância = velocidade/tempo
        speed = d_meters * time_constant

        return int(speed)

    def format_trajectories(self):
        output_dict = {}

        for key, value in self.track_history.items():
            novo_valor = [{"x": x, "y": y} for x, y in value]
            output_dict[key] = novo_valor

        return output_dict

    def format_velocity(self):
        resultado = {}

        for chave, lista in self.speed_history.items():
            valores_nao_nulos = [valor for valor in lista if valor != 0]
            if valores_nao_nulos:
                resultado[chave] = sum(valores_nao_nulos) / len(valores_nao_nulos)
            else:
                resultado[chave] = 0

        return resultado

    def format_start_time(self):
        resultado = {}

        for chave, valores in self.start_time.items():
            if valores:
                resultado[chave] = valores[0]
            else:
                resultado[chave] = ""

        return resultado

    def format_end_time(self):
        resultado = {}

        for chave, valores in self.end_time.items():
            if valores:
                resultado[chave] = valores[0]
            else:
                resultado[chave] = ""

        return resultado

    def format_classes(self):
        resultado = {}

        for chave, valores in self.classes_history.items():
            if valores:
                resultado[chave] = valores[0]
            else:
                resultado[chave] = ""

        return resultado

    def format_data_to_DB(self, input_data):
        grouped_data = {}

        for index in input_data["track_history"]:
            grouped_object = {
                "trajetorias": input_data["track_history"][index],
                "velocidade": input_data["speed_history"][index],
                "tipo": input_data["classes_history"][index],
                "start_time": input_data["start_time"][index],
                "end_time": input_data["end_time"][index],
            }

            grouped_data[index] = grouped_object

        result_array = list(grouped_data.values())

        return result_array

    def process(self, video_data):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(video_data.read())
                temp_file_path = temp_file.name

            cap = cv2.VideoCapture(temp_file_path)

            if cap.isOpened() == False:
                raise Exception("Não foi possível abrir captura")

            # Loop through the video frames
            while cap.isOpened():
                # Read a frame from the video
                success, frame = cap.read()

                if success:
                    # Run YOLOv8 tracking on the frame, persisting tracks between frames
                    results = self.model.track(frame, persist=True)

                    a = len(results[0])
                    if a != 0:
                        # Get the boxes and track IDs
                        boxes = results[0].boxes.xywh.cpu()
                        track_ids = results[0].boxes.id.int().cpu().tolist()

                        # Get Classes, names and confidences
                        classes = results[0].boxes.cls.cpu().tolist()
                        names = results[0].names

                        # Plot the tracks
                        for box, track_id, clas in zip(boxes, track_ids, classes):
                            x, y, w, h = box
                            track = self.track_history[track_id]
                            track.append((float(x), float(y)))  # x, y center point

                            speed = self.speed_history[track_id]

                            tipo = self.classes_history[track_id]
                            if len(tipo) == 0:
                                tipo.append(names[clas])

                            st = self.start_time[track_id]
                            if len(st) == 0:
                                st.append(
                                    datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
                                )
                            self.end_time[track_id] = datetime.now().strftime(
                                "%Y-%m-%dT%H:%M:%S.%f"
                            )

                            points = (
                                np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                            )
                            teste = np.hstack(track).astype(np.int32)

                            if len(teste) >= 4:
                                obj_speed = self.estimatespeed(
                                    [teste[len(teste) - 4], teste[len(teste) - 3]],
                                    [teste[len(teste) - 2], teste[len(teste) - 1]],
                                )
                                speed.append(obj_speed)

                else:
                    # Break the loop if the end of the video is reached
                    break

            # Release the video capture object
            cap.release()

            results_data = {
                "track_history": self.format_trajectories(),
                "speed_history": self.format_velocity(),
                "classes_history": self.format_classes(),
                "start_time": self.format_start_time(),
                "end_time": self.end_time,
            }

            output_data = self.format_data_to_DB(results_data)

            return output_data
        except Exception as e:
            raise Exception("Não foi possível abrir captura")


class HelmetProcessing:
    def __init__(self, model_path="best.pt"):
        self.model = YOLO("best.pt")

    def process(self, video_data):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(video_data.read())
                temp_file_path = temp_file.name

            cap = cv2.VideoCapture(temp_file_path)

            frame_classes = []

            if cap.isOpened() == False:
                raise Exception("Não foi possível abrir captura")

            while cap.isOpened():
                success, frame = cap.read()

                if success:
                    results = self.model(frame)
                    classes = results[0].boxes.cls.cpu().tolist()

                    for clas in classes:
                        frame_classes.append(clas)
                else:
                    break

            cap.release()

            total_com_capacete = 0
            total_sem_capacete = 0
            for i in frame_classes:
                if i == 0:
                    total_com_capacete += 1
                else:
                    total_sem_capacete += 1

            dicionario = {
                "total_com_capacete": total_com_capacete,
                "total_sem_capacete": total_sem_capacete,
            }

            return dicionario
        except Exception as e:
            raise Exception("Não foi possível abrir captura")
