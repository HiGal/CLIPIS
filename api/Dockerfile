FROM python:3.8
WORKDIR /api
COPY . /api
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
