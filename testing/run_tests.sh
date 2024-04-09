# This file presents how to automatically run the tests

cd ..
docker build -t nillion-python-starter -f testing/Dockerfile .
docker run -it --rm nillion-python-starter bash /home/vscode/testing/docker_main.sh
