FROM python:3.9.6-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Copy local code to the container image.
WORKDIR /birb
COPY . /birb
EXPOSE $PORT
# Install production dependencies.
RUN apt-get update; apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch==1.9.0+cpu torchvision==0.10.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pwd; ls

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 webhook:app
