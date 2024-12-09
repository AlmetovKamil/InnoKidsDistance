FROM ghcr.io/osgeo/gdal:ubuntu-full-3.9.2 AS base

ARG PYTHON_VERSION=3.12.3

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y locales \
    && echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen ru_RU.UTF-8 \
    && groupadd --gid 1001 inno \
    && useradd --uid 1001 --gid 1001 -m -d /home/inno inno \
    && mkdir /app \
    && chown -R inno:inno /app \
    && apt-get install -y libffi-dev build-essential make autoconf gcc g++ libssl-dev xz-utils \
    zlib1g zlib1g-dev cmake libgeos-dev libproj-dev ninja-build wget libjson-c-dev \
    libjsoncpp-dev libbrotli-dev libgeos-dev libproj-dev libjson-c-dev libxml2-dev curl \
    libzstd-dev libmagic1

RUN wget -q https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz \
    && tar xf Python-${PYTHON_VERSION}.tar.xz \
    && cd Python-${PYTHON_VERSION} \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make install \
    && cd .. && rm -rf Python-${PYTHON_VERSION} && rm -rf Python-${PYTHON_VERSION}.tar.xz \
    && apt-get remove -y make autoconf build-essential && apt-get autoremove -y  \
    && apt-get autoclean -y && apt-get autoremove -y && apt-get clean && rm -rf /var/cache/apt/*

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:git-core/ppa \
    && apt-get update \
    && apt-get install -y git

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PIP_USER=true

ENV PIP_NO_CACHE_DIR=1
ENV PATH=/home/inno/.local/bin:$PATH

FROM base AS base_api

USER inno
WORKDIR /app

ARG PYTHONPATH="${HOME}/.local/lib/python3.12/site-packages/"

COPY requirements.txt .
RUN pip3 install -U pip setuptools \
    && pip3 install -U pip-tools \
    && pip3 install --no-cache-dir -r requirements.txt

COPY ./ /app/

FROM base_api AS api

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
