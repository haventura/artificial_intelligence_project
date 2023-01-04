FROM python:3.10-slim

EXPOSE 8501

RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 poppler-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]