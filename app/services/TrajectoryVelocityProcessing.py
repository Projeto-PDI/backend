from collections import defaultdict
from datetime import datetime
import cv2
import numpy as np
import math
import json
from json import JSONEncoder
from io import BytesIO
import tempfile

from ultralytics import YOLO

class DateTimeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

class TrajectoryVelocityProcessing:
    def __init__(self, model_path='yolov8n.pt'):
        # Load the YOLOv8 model
        self.model = YOLO('yolov8n.pt')

        # Store the track history
        self.track_history = defaultdict(lambda: [])
        self.speed_history = defaultdict(lambda: [])
        self.start_time = defaultdict(lambda: [])
        self.end_time = defaultdict(lambda: [])

    def estimatespeed(self, Location1, Location2):
        # Euclidean Distance Formula
        d_pixel = math.sqrt(math.pow(Location2[0] - Location1[0], 2) + math.pow(Location2[1] - Location1[1], 2))
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

    def process(self, video_data):
        try:
            # Cria um arquivo temporário para armazenar o conteúdo do vídeo
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(video_data.read())
                temp_file_path = temp_file.name

            # Leitura do arquivo temporário usando VideoCapture
            cap = cv2.VideoCapture(temp_file_path)

            if cap.isOpened() == False:
                raise Exception('Não foi possível abrir captura')

            # Loop through the video frames
            while cap.isOpened():
                # Read a frame from the video
                success, frame = cap.read()

                if success:
                    # Run YOLOv8 tracking on the frame, persisting tracks between frames
                    results = self.model.track(frame, persist=True)

                    # Get the boxes and track IDs
                    boxes = results[0].boxes.xywh.cpu()
                    track_ids = results[0].boxes.id.int().cpu().tolist()

                    # Plot the tracks
                    for box, track_id in zip(boxes, track_ids):
                        x, y, w, h = box
                        track = self.track_history[track_id]
                        speed = self.speed_history[track_id]
                        track.append((float(x), float(y)))  # x, y center point

                        st = self.start_time[track_id]
                        if len(st) == 0:
                            st.append(datetime.now())
                        self.end_time[track_id] = datetime.now()

                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        teste = np.hstack(track).astype(np.int32)

                        if len(teste) >= 4:
                            obj_speed = self.estimatespeed([teste[len(teste) - 4], teste[len(teste) - 3]],
                                                    [teste[len(teste) - 2], teste[len(teste) - 1]])
                            speed.append(obj_speed)

                else:
                    # Break the loop if the end of the video is reached
                    break

            # Release the video capture object
            cap.release()

            results_data = {
                'track_history': self.format_trajectories(), 
                'speed_history': self.format_velocity(),
                'start_time': self.start_time, 
                'end_time': self.end_time
            }
            
            return results_data
        except:
            return {"error": "Erro ao processar vídeo"}
    

if __name__ == "__main__":
    # Exemplo de uso da classe
    speed_estimator = TrajectoryVelocityProcessing()

    video_path = 'C:\\Users\\mauriciosantos\\Downloads\\video.mp4'
    
    json_filename = 'results.json'

    results_data = speed_estimator.process(video_path)

    # Salve os resultados em um arquivo JSON
    with open(json_filename, 'w') as json_file:
        json.dump(results_data, json_file, cls=DateTimeEncoder)