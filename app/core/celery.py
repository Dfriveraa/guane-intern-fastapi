from celery import Celery

CELERY_BROKER = f"amqp://user:bitnami@rabbitmq:5672//"
CELERY_BACKEND = f"redis://:password123@redis:6379/0"

celery_config = {
    "broker_url": CELERY_BROKER,
    "result_backend": CELERY_BACKEND,
    "result_expires": 7200,  # in secs
}
celery_app = Celery(__name__, config_source=celery_config)
celery_app.conf.task_routes = {
    "app.workers.dogs.create_dog_worker": "test-queue"}

celery_app.conf.update(task_track_started=True)
