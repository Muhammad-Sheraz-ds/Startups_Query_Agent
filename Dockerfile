FROM python:3.9-slim
WORKDIR /app
COPY ./backend/ .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
