FROM python:3.8
WORKDIR /api
COPY . /api
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "172.19.0.5", "--port", "80"]
