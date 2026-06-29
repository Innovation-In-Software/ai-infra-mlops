FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir \
    "flask>=3.0" \
    "joblib>=1.3" \
    "scikit-learn>=1.3.0,<1.6" \
    "numpy>=1.24" \
    "pandas>=2.0"
COPY workspace/lab5/models/best_model.pkl /app/model.pkl
COPY lab5/src/serve.py /app/serve.py
RUN chmod a+r /app/model.pkl /app/serve.py
ENV PYTHONUNBUFFERED=1
USER 1000
EXPOSE 8080
CMD ["python", "serve.py"]
