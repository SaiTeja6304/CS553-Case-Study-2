#!/bin/bash

set -eou pipefail

echo "Deploying frontend..."

echo "Setting up SSH"

USER="group11"
PORT="22000"
FRONTEND_PORT="7011"
HOST_ADDRESS="0.0.0.0"
SERVER="paffenroth-23.dyn.wpi.edu"
KEY_PATH="./ssh_keys/group_key"
LOCAL_DIR="./CS553-Case-Study-2/frontend/."
REMOTE_DIR="./CS553-Case-Study-2/frontend"

SCP_BASE = (scp -i "${KEY_PATH}" -P "${PORT}" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "${USER}"@"${SERVER}")

echo "Performing SSH"

ssh -i "${KEY_PATH}" -p "${PORT}" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "${USER}"@"${SERVER}"

echo "Copying frontend files to remote server..."

rm -rf \"${REMOTE_DIR}\" && mkdir -p \"${REMOTE_DIR}\"
"${SCP_BASE[@]}" -r "${LOCAL_DIR}" "${USER}@${SERVER}:${REMOTE_DIR}"

echo "Installing API packages"

sudo apt update
sudo apt install -y tmux python3 python3-venv python3-pip

echo "Creating python virtual environment and intalling libraries"

cd "${REMOTE_DIR}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip --no-cache-dir
pip install -r requirements.txt --no-cache-dir

echo "Starting frontend app"

sudo fuser -k ${FRONTEND_PORT}/tcp || true
tmux kill-session -t frontend-11 || true
tmux new -d -s frontend-11
streamlit run src/streamlit_app.py --server.port ${FRONTEND_PORT} --server.address ${HOST_ADDRESS}

echo "Done"