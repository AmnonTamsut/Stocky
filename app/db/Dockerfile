# Use an official MongoDB base image
FROM mongo:7.0
WORKDIR /app
# Expose the default MongoDB port (27017)
EXPOSE 27017



RUN apt-get update && apt-get install -y python3-pip

# Copy any custom configuration files (if needed)
# COPY mongod.conf /etc/mongod.conf
COPY requirements.txt /db/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /db/requirements.txt
COPY . .


# Start the MongoDB server
CMD ["mongod"]
