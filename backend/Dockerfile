FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
COPY api_foodgram .
RUN python3 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir && \
    python3 manage.py collectstatic --noinput
CMD python3 manage.py migrate --noinput && \
    gunicorn api_foodgram.wsgi:application --bind 0.0.0.0:8000