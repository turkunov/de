FROM python:3.9-alpine

# Create unprivileged user
RUN adduser -D appuser

# Set working directory
WORKDIR /python_app

# Copy application
COPY . .

# install packages
RUN apk add postgresql-dev python3-dev \
    && python3 -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del python3-dev \
    && rm -rf /var/cache/apk/*

# Set permissions
RUN chown -R appuser:appuser /python_app
USER appuser

RUN chmod +x entrypoint.sh

# Set entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]