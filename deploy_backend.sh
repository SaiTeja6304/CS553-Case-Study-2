#!/bin/bash

set -eou pipefail

git clone https://github.com/SaiTeja6304/CS553-Case-Study-2.git
cd CS553-Case-Study-2

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


# Prompt for token securely
read -s -p "Enter HuggingFace Token: " HF_TOKEN
echo
echo "HF_TOKEN=$HF_TOKEN" > .env

# Run backend
uvicorn backend.src.app:app --host 0.0.0.0 --port 9011 --reload