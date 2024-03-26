from celery import Celery

#configure Celery to use your chosen message broker for Redis (fair round robin):
celery_app = Celery('my_ml_app', broker='redis://localhost:6379/0')

#RabbitMQ -- uses FIFO so redis was selected instead for stability:
#celery_app = Celery('my_ml_app', broker='amqp://guest:guest@localhost')

@celery_app.task
def process_inference_request(image_id):
    # TODO: logic to process an inference request
    print(f"Processing inference request for image_id: {image_id}")

@celery_app.task
def process_training_request(dataset_id):
    # TODO: logic to process a training request
    print(f"Processing training request for dataset_id: {dataset_id}")
