FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir \
    "flask>=3.0" \
    "joblib>=1.3" \
    "scikit-learn>=1.6.0,<2.0" \
    "numpy>=1.24" \
    "pandas>=2.0"
COPY workspace/lab5/models/best_model.pkl /app/model.pkl
COPY lab5/src/serve.py /app/serve.py
COPY lab5/src/serve /usr/local/bin/serve
RUN chmod a+r /app/model.pkl /app/serve.py && chmod a+x /usr/local/bin/serve
ENV PYTHONUNBUFFERED=1
ENV SAGEMAKER_BIND_TO_PORT=8080
USER 1000
EXPOSE 8080
CMD ["serve"]
