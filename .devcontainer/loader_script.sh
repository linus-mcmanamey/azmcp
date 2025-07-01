#!/bin/bash
set -e



curl -sS https://raw.githubusercontent.com/diogocavilha/fancy-git/master/install.sh | sh
cp /tmp/app_config ~/.fancy-git/app_config
git config --global credential.helper store
git config --global credential.interactive auto
git config --global credential.useHttpPath true
git config --global user.email "linus.mcmanamey@gmail.com"
git config --global user.name "linus-mcmanamey"
git config --global init.defaultBranch main
##git config --global --add safe.directory /workspaces/*
git config --global http.proxy http://proxy.police.tas.gov.au:8080
git config --global https.proxy http://proxy.police.tas.gov.au:8080
git config --global http.noProxy localhost,127.0.0.1,.local  # Added line to bypass proxy for local addresses

SSH_CONFIG="$HOME/.ssh/config"
HOST_TO_CHECK="ssh.dev.azure.com"

# Function to write SSH config
write_ssh_config() {
    echo "Host $HOST_TO_CHECK" >> "$SSH_CONFIG"
    echo "    IdentityFile ~/.ssh/id_rsa" >> "$SSH_CONFIG"
    echo "    IdentitiesOnly yes" >> "$SSH_CONFIG"
    echo "    HostkeyAlgorithms +ssh-rsa" >> "$SSH_CONFIG"
    echo "    PubkeyAcceptedKeyTypes=ssh-rsa" >> "$SSH_CONFIG"
    echo "    ProxyCommand corkscrew inthaproxy.ems.tas.gov.au 8080 %h %p" >> "$SSH_CONFIG"
}

# Create SSH config directory if it doesn't exist
#mkdir -p "$HOME/.ssh"

# If config file doesn't exist, create it and write config
if [ ! -e "$SSH_CONFIG" ]; then
    write_ssh_config
else
    # Check if Host entry exists
    if ! grep -q "^Host $HOST_TO_CHECK\$" "$SSH_CONFIG"; then
        write_ssh_config
    fi
fi
# Set appropriate permissions
#chmod 700 "$SSH_CONFIG"


# Add SSH agent management with session persistence to avoid repeated authentication
cat >> ~/.bashrc << 'EOF'

# SSH Agent management - only start if not already running
if [ -z "$SSH_AUTH_SOCK" ] || [ ! -S "$SSH_AUTH_SOCK" ]; then
    # Check if there's already an agent running
    if [ -f ~/.ssh/agent-environment ]; then
        source ~/.ssh/agent-environment > /dev/null
    fi

    # Test if the agent is still valid
    if ! ssh-add -l > /dev/null 2>&1; then
        # Start new agent and save environment
        eval "$(ssh-agent -s)" > /dev/null
        echo "export SSH_AUTH_SOCK=$SSH_AUTH_SOCK" > ~/.ssh/agent-environment
        echo "export SSH_AGENT_PID=$SSH_AGENT_PID" >> ~/.ssh/agent-environment

        # Only add key if it exists and is not already loaded
        if [ -f ~/.ssh/id_rsa ] && ! ssh-add -l | grep -q ~/.ssh/id_rsa; then
            ssh-add ~/.ssh/id_rsa 2>/dev/null || true
        fi
    fi
fi
EOF

# Add useful aliases
echo "alias ll='ls -l'" >> ~/.bashrc
echo "alias la='ls -A'" >> ~/.bashrc
echo "alias l='ls -CF'" >> ~/.bashrc
echo "alias python=python3" >> ~/.bashrc
echo "alias pip=pip3" >> ~/.bashrc

# Create SSH directory if needed
mkdir -p ~/.ssh
chmod 700 ~/.ssh


# uv init --package azmcp
#uv add mcp httpx asyncio-stdio pydantic "typer[all]"
pip install --system -r /tmp/requirements.txt
# Add development dependencies
#uv add --dev pytest pytest-asyncio black ruff mypy build twine


ln -sf /workspaces/textual /workspaces/azmcp/textual
# Generate lock file
uv lock
pre-commit autoupdate
pre-commit install
pre-commit run --all-files -v
kinit $USERNAME@POLICE.TAS.GOV.AU
source ~/.bashrc
