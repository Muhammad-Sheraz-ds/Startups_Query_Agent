



# backend/Dockerfile

FROM python:3.10-slim

# Install system dependencies if needed
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy root-level and backend requirements, then install them
COPY requirements.txt .
COPY backend/requirements.txt ./backend/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r backend/requirements.txt

#RUN curl -sSL https://ollama.com/install.sh | sh

# (Optional) If Ollama CLI is supported and you want to pull the model automatically:
#RUN ollama pull llama3.2

# Copy the entire project into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Start the FastAPI server using uvicorn
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
