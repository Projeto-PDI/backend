FROM python:3.11
WORKDIR /code
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run", "--port=5000"]
