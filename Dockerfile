FROM python:3.13-slim

WORKDIR /lazyjobfinder

RUN apt-get update && apt-get install -y \
    curl build-essential gcc libffi-dev \
 && curl -LsSf https://astral.sh/uv/install.sh | bash \
 && cp /root/.local/bin/uv /usr/local/bin/uv \
 # in order to install psycopg2 from source I need the following:
 && apt-get install libpq-dev python3-dev -y

COPY . .

RUN uv sync

RUN apt-get remove -y curl build-essential gcc libffi-dev \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["uv", "run", "main.py"]
