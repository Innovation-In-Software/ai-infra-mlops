FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask joblib scikit-learn numpy pandas
COPY workspace/lab5/models/best_model.pkl /app/model.pkl
COPY lab5/src/serve.py /app/serve.py
USER 1000
EXPOSE 8080
CMD ["python", "serve.py"]
