#!/usr/bin/env bash
# Yerel: medicalsearch (8501) ile çakışmaz. Streamlit Cloud bu dosyayı kullanmaz; orada varsayılan port geçerli.
set -euo pipefail
cd "$(dirname "$0")"
exec streamlit run streamlit_app.py --server.port 9517 --server.address localhost
