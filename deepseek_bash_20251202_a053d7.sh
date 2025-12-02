# ודא שיש HF_TOKEN
export HF_TOKEN="hf_your_token_here"

# הרץ את השירות
docker-compose up -d

# בדוק סטטוס
docker-compose ps

# בדוק logs
docker-compose logs -f