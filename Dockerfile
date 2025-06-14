FROM python:3.9
WORKDIR /MusicRecBack
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# RUN ["apt-get", "update"]
# RUN ["apt-get", "install", "-y", "vim"]
# CMD ["uvicorn", "app.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80","--reload"]
CMD ["uvicorn", "app.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["gunicorn", "app.app:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]
