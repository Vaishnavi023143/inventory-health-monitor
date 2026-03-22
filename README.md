cd ~/Desktop/inventory-health-monitor
python3 -m venv .venv
source .venv/bin/activate
pip install pandas openpyxl
pip freeze > requirements.txt
