# specify base image for python
FROM python:3.14-slim

# select working directory
WORKDIR /app

# copy requirements txt
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the code
COPY . .

# Expose port
EXPOSE 8006

# run fastapi server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8006"]