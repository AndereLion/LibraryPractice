FROM python:3.11.1-alpine
LABEL maintainer="GolfTeam"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /api/library_practice/

COPY requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r ./requirements.txt


ENV PATH="/api/library_practice:${PATH}"

COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh

COPY . .

RUN apk add bash

EXPOSE 8000

ENTRYPOINT ["bash", "/api/library_practice/entrypoint.sh"]
