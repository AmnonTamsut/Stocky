FROM python:3.8

WORKDIR /app
EXPOSE 4321

#RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4321"]
