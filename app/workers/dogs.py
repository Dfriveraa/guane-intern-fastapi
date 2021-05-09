import asyncio

from celery import current_task

from app.core.celery import celery_app
from app.services.dog import dog_service


@celery_app.task(acks_late=True)
def create_dog_worker(name: str, publisher_id: int):
    print(name)
    print(publisher_id)
    current_task.update_state(state='progress')
    # time.sleep(15)
    b = asyncio.run(dog_service.find_dog_by_name(name=name))
    # current_task.update_state(state='finishing')
    return True
