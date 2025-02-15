# frontend/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Copy frontend-specific requirements and install them
COPY frontend/requirements.txt ./frontend/
RUN pip install --upgrade pip && \
    pip install -r frontend/requirements.txt

# Copy the frontend code
COPY frontend/ /app/frontend/

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app using Python's module system
CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.enableCORS=false"]
