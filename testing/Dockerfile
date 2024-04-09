FROM mcr.microsoft.com/devcontainers/python

USER vscode

# Add Foundry and Nilup to Path 
ENV PATH="$PATH:/home/vscode/.foundry/bin:/home/vscode/.nilup/bin:/home/vscode/.local/bin"

# Install Nilup
RUN curl https://nilup.nilogy.xyz/install.sh | bash && \
    nilup install latest && \
    nilup use latest && \
    nilup init

# Install foundry
RUN curl -L https://foundry.paradigm.xyz | bash && \
    bash -c "foundryup"

WORKDIR /home/vscode
COPY --chown=vscode:vscode . .
