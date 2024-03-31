FROM python:3.8

# Set working directory
WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip
EXPOSE 8501
# Copy requirements.txt and install dependencies
COPY requirements.txt /frontend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /frontend/requirements.txt



COPY . .

# Run the Streamlit app
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]