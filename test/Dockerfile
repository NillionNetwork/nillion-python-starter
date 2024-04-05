FROM mcr.microsoft.com/devcontainers/python

# Install npm
RUN apt-get update && \
    apt-get install -y npm && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

USER vscode

# Add Foundry and Nilup to Path 
ENV PATH="$PATH:/home/vscode/.foundry/bin:/home/vscode/.nilup/bin"

# Install AWS CLI
RUN pipx install awscli

# Install Nilup
RUN curl https://nilup.nilogy.xyz/install.sh | bash && \
nilup install latest && \
nilup use latest && \
nilup init

# Install foundry
RUN curl -L https://foundry.paradigm.xyz | bash && \
 bash -c "foundryup"