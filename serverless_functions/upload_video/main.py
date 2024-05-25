import json
import os
import uuid

from google.cloud import storage, pubsub_v1
from google.api_core.retry import Retry
from flask import jsonify, Request, Flask

from library_serverless_core.persistence.database import open_session
from library_serverless_core.security.token_utils import verify_token
from library_serverless_core.shared_models.User import User
from library_serverless_core.shared_models.Video import Video, VideoStatus


BUCKET_NAME: str = os.environ.get('DRONE_BUCKET', 'video-drone')
PATH_TO_VIDEOS: str = os.environ.get('DRONE_PATH_TO_VIDEOS', 'videos')
PROJECT_ID: str = os.environ.get('PROJECT_ID', 'misw-4204-nube')
VIDEO_PROCESS_TOPIC_ID: str = os.environ.get('VIDEO_PROCESS_TOPIC_ID', 'process-video-request')


app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_video(request: Request):
    if request.method != 'POST':
        return jsonify(''), 404

    payload = verify_token(request.values['token'])
    if not payload:
        return jsonify(''), 505

    user_id = payload['user_id']
    description = request.values['description']
    video_file = request.files['video']
    video_name = uuid.uuid4().__str__()

    with open_session() as session:
        user = session.query(User).filter_by(id=user_id).first()

        if description:
            new_video = Video(
                description=description,
                video_id=video_name,
                path='',
                user_id=user.id,
                status=VideoStatus.uploaded
            )
            session.add(new_video)
            session.commit()

        print('created video')

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f'{PATH_TO_VIDEOS}/{video_name}')
    blob.upload_from_string(video_file.read(), content_type='video/mp4', retry=Retry(total=15, backoff_factor=0.1))

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, VIDEO_PROCESS_TOPIC_ID)

    data: dict = {'filename': video_name}
    future = publisher.publish(topic_path, json.dumps(data).encode('utf-8'))

    print(f'published message id {future.result()}')

    return jsonify({
        'success': True,
        'video_id': video_name,
        'status': VideoStatus.uploaded.name
    }), 505


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

