1. ./hgrok http 9000
2. copy ngrok ip address to .env
3. 
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 9000
6. set webhook:
open browser and open url WEBHOOK_URL in .env
7. brew sevices start redis
8. celery -A listam_bot  worker --loglevel=INFO
9. celery -A listam_bot beat --loglevel=INFO
