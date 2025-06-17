FROM python:3.11.9-slim-bookworm AS base

ARG DJANGO_ENV
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV=${DJANGO_ENV}

# -----------------------------------------------------------------------------
FROM base AS builder
RUN apt-get update && \
    apt-get install -y libpq-dev

COPY requirements requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip wheel --no-cache-dir --wheel-dir=/usr/src/app/wheels -r \
    requirements/${BUILD_ENV}.txt

# -----------------------------------------------------------------------------
FROM base AS runner

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client-15 \
    libpq5 \
    cron && \
    apt-get autoremove -y &&\
    apt-get clean -y &&\
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/
    
WORKDIR /app/mepa-api
COPY ./ ./

COPY cronjob/cronjob /etc/cron.d/mec-cron
RUN chmod -R 755 /etc/cron.d/mec-cron && \
    /usr/bin/crontab /etc/cron.d/mec-cron

CMD ["cron", "-f"]
