cd /tmp/ && \
git clone https://github.com/NillionNetwork/nillion-python-starter.git && \
cd nillion-python-starter && \
cp .env.sample .env && \
python3 -m pip install -r requirements.txt && \
bash ./create_venv.sh && \
./bootstrap-local-environment.sh && \
echo "Waiting 60 seconds for preprocessing elements" && sleep 60 && \
sh compile_programs.sh && \
cd client_single_party_compute && \
for file in `ls *.py`; do echo "$file\n\n" && python3 $file && echo "[DONE] $file"; done && \
killall nillion-devnet && \
rm -rf /tmp/nillion-python-starter