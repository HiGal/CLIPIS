FROM continuumio/miniconda3
WORKDIR /api
COPY . /api
RUN pip install -r requirements.txt
RUN conda install -c pytorch faiss-cpu
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
