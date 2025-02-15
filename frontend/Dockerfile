# frontend/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Copy and install frontend requirements
COPY frontend/requirements.txt ./frontend/
RUN pip install --upgrade pip && \
    pip install -r frontend/requirements.txt

# Copy the Streamlit app code
COPY frontend/ /app/frontend/

# Expose the Streamlit port
EXPOSE 8501

# Start the Streamlit app (CORS disabled)
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.enableCORS=false"]
