import functions_framework
import os

from google.cloud import storage
from flask import jsonify

from library_serverless_core.persistence.database import open_session
from library_serverless_core.security.token_utils import decode_token
from library_serverless_core.shared_models.Video import Video

BUCKET_NAME: str = os.environ.get('DRONE_BUCKET')
PATH_TO_VIDEOS: str = os.environ.get('DRONE_PATH_TO_VIDEOS')


@functions_framework.http
def delete_one_video(request):
    if request.method != 'DELETE':
        return jsonify(''), 404

    payload = decode_token(request.headers['Pascal'])
    if not payload:
        return jsonify(''), 505

    video_id = request.args.get('video-id')
    user_id = payload['user_id']

    with open_session() as session:
        video = session.query(Video).filter(Video.id == video_id).first()

        if video is None:
            return jsonify({'message': 'Invalid task id'}), 401

        if video.status.name == 'uploaded':
            return jsonify({'message': 'Video is being processed, cannot delete it'})

        if video.user_id != user_id:
            return jsonify(''), 404

        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        edited_video = bucket.blob(f'{PATH_TO_VIDEOS}/{video.path.split("/")[-1]}')
        original_video = bucket.blob(f'{PATH_TO_VIDEOS}/{video.video_id}')

        edited_video.delete()
        original_video.delete()

        session.delete(video)
        session.commit()
        return jsonify({'message': f'Video deleted successfully `{video.video_id}`'}), 200
