# 1. pyhton manage.py runserver

# 2. RabbitMQ --> sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management

# 3. Celery Worker --> celery -A djangoProject worker -l info

# 4. Flower -->  celery -A djangoProject flower

# 5. WebHook -->  stripe listen --forward-to localhost:8000//payment/webhook/ 
