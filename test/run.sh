# This file presents how to automatically run the tests

docker build . -t nillion-python-starter
docker run -it --rm nillion-python-starter bash /home/vscode/test_python.sh