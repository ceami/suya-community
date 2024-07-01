# Use an official Python runtime as the base image
FROM python:3.11.0-slim

# Set the working directory in the container
WORKDIR /opt/info_reels_docker

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .


# Install dependencies
RUN set -xe \
    && apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2\
    && apt-get install -y --no-install-recommends build-essential \
    && pip install virtualenvwrapper poetry==1.4.2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry install --no-root

# Copy project files
COPY ["README.md", "Makefile", "./"]
COPY info_reels_docker info_reels_docker

# Expose the Django development server port (adjust if needed)
EXPOSE 8080

## Set up the entrypoint
#COPY scripts scripts
#RUN chmod a+x scripts/entrypoint.sh
#
#CMD cd scripts
#ENTRYPOINT ["entrypoint.sh"]
CMD make run-server
