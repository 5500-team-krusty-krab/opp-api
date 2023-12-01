# 
FROM python:3.11

# Set work path as /app
WORKDIR /app

# Copy current content to /app container
COPY . /app

# Install packages in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define the command line
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
