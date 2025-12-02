# 1. התקן את התלויות
pip install -r requirements.txt

# 2. הרץ את המערכת
python main.py

# 3. או הרץ עם Docker
docker build -t abraham-ai .
docker run -p 8000:8000 abraham-ai