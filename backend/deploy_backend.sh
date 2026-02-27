#!/bin/bash

set -eou pipefail

echo "Deploying backend..."

echo "Setting up SSH"

USER="group11"
PORT="22011"
BACKEND_PORT="9011"
HOST_ADDRESS="0.0.0.0"
SERVER="paffenroth-23.dyn.wpi.edu"
KEY_PATH="./ssh_keys/secure_key"
LOCAL_DIR="./CS553-Case-Study-2/backend/."
REMOTE_DIR="./CS553-Case-Study-2/backend"

SCP_BASE = (scp -i "${KEY_PATH}" -P "${PORT}" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "${USER}"@"${SERVER}")

echo "Performing SSH"

ssh -i "${KEY_PATH}" -p "${PORT}" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "${USER}"@"${SERVER}"

echo "Copying backend files to remote server..."

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

echo "Starting backend app"

pkill -f uvicorn || true
sudo fuser -k ${BACKEND_PORT}/tcp || true
tmux kill-session -t backend-11 || true
tmux new -d -s backend-11
uvicorn src.app:app --host ${HOST_ADDRESS} --port ${BACKEND_PORT} --reload

echo "Done"