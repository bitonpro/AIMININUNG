# 1. צור README.md בסיסי
echo "# AIMININUNG - AI Mining & Cloud Infrastructure" > README.md
echo "## פרויקט ניהול ענן AI וכרייה מתקדם" >> README.md

# 2. עדכן .gitignore
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Docker
*.dockerignore
.env

# System
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Secrets
*.pem
*.key
*.cert
secrets.ini
config.local.*
EOL

# 3. הוסף רישיון בסיסי
curl -o LICENSE https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/mit.txt