FROM python:3.11-slim

WORKDIR /app

# Copy backend script
COPY streamlit_backend.py .

# Install dependencies
RUN pip install --no-cache-dir \
    a2a-sdk==1.0.1 \
    langchain-groq \
    langchain-core \
    uvicorn \
    starlette \
    psutil \
    httpx \
    python-dotenv

EXPOSE 9000

CMD ["python", "streamlit_backend.py"]
