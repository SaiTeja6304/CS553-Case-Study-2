#!/bin/bash

set -eou pipefail

git clone https://github.com/SaiTeja6304/CS553-Case-Study-2.git
cd CS553-Case-Study-2

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


# Run frontend
streamlit run frontend/streamlit_app.py --server.port 7011 --server.address 0.0.0.0