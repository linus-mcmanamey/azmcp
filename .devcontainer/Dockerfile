FROM mcr.microsoft.com/devcontainers/python:1-3.12

USER root

COPY .devcontainer/kbr5.conf /etc/krb5.conf
COPY .devcontainer/config/fancygit/app_config /tmp
COPY .devcontainer/requirements.txt /tmp/requirements.txt
# Set proxy environment variables
ENV http_proxy=http://proxy.police.tas.gov.au:8080
ENV https_proxy=http://proxy.police.tas.gov.au:8080
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    build-essential \
    fontconfig \
    make \
    htop \
    krb5-user \
    libkrb5-dev \
    unixodbc \
    unixodbc-dev \
    gnupg2 \
    ca-certificates \
    openssl \
    corkscrew \
    odbcinst \
    openssh-client \
    libmemcached-dev \
    jq \
    sqlite3 \
    redis-tools \
    && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - \
    && apt-get install -y nodejs \
    && apt-get -y clean

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy requirements file and install dependencies with uv

RUN uv pip install --system --upgrade pip
RUN uv pip install --system -r /tmp/requirements.txt

# Create workspaces directory and clone textual repo
RUN git clone https://github.com/Textualize/textual.git /workspaces/textual

# Create soft link to textual repo in azmcp workspace
#RUN ln -sf /workspaces/textual /workspaces/azmcp/textual

CMD ["/bin/bash"]
