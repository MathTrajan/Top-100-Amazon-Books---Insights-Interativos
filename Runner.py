import sys
from streamlit.web import cli as stcli

sys.argv = ["streamlit", "run", "top100.py"]  # Ajuste o nome do arquivo
sys.exit(stcli.main())
