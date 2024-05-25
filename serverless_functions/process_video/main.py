import base64
import json
import logging
import os

from google.cloud import storage

from library_serverless_core.persistence.database import open_session
from library_serverless_core.shared_models.Video import Video
from video_processing import process_video as process

BUCKET_NAME: str = os.environ.get('DRONE_BUCKET', 'video-drone')
PATH_TO_VIDEOS: str = os.environ.get('DRONE_PATH_TO_VIDEOS', 'videos')
PROJECT_ID: str = os.environ.get('PROJECT_ID', 'misw-4204-nube')
VIDEO_PROCESS_TOPIC_ID: str = os.environ.get('VIDEO_PROCESS_TOPIC_ID', 'process-video-request')

logging.basicConfig(level=logging.INFO)


def process_video_task(filename: str):
    local_file_path = f'/tmp/{filename}'
    cloud_file_path = f'{PATH_TO_VIDEOS}/{filename}'

    logging.log(level=logging.INFO, msg=f'local file path {local_file_path}')

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    cloud_blob = bucket.blob(cloud_file_path)
    cloud_blob.download_to_filename(local_file_path)

    data: dict = process(file_path=local_file_path, image_path='./static/img/logo.jpeg')

    blob = bucket.blob(f'{PATH_TO_VIDEOS}/{data["edited_video_name"]}')
    blob.upload_from_filename(data['new_file_path'], content_type='video/mp4')
    logging.log(level=logging.INFO, msg=f'Video processed {filename}')

    # clear storage in the device containing the worker
    os.remove(local_file_path)
    os.remove(data['new_file_path'])
    logging.log(level=logging.INFO, msg=f'Freed local storage {local_file_path}, {data["new_file_path"]}')

    return data


def process_video(event, context):
    """
    Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    if 'data' in event:
        body = base64.b64decode(event['data']).decode('utf-8')
        json_received = json.loads(body)

        logging.log(level=logging.INFO, msg=f'Received: {body}.')

        data: dict = process_video_task(json_received['filename'])

        with open_session() as session:
            video = session.query(Video).filter(Video.video_id == json_received['filename']).first()
            video.status = 'processed'
            video.path = data['new_file_path']
            session.add(video)
            session.commit()
    else:
        logging.log(level=logging.INFO, msg=f'No messages received for worker consumer.')
