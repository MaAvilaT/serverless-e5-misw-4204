import functions_framework
from flask import jsonify, Request

from library_serverless_core.persistence.database import open_session
from library_serverless_core.security.token_utils import verify_token
from library_serverless_core.shared_models.Video import Video, VideoStatus


@functions_framework.http
def get_one_video(request: Request):
    if request.method != 'GET':
        return jsonify(''), 404

    if not verify_token(request.headers['Pascal']):
        return jsonify(''), 505

    video_id = request.args.get('video-id')

    with open_session() as session:
        video = session.query(Video).filter(Video.id == video_id).first()

        if video is None:
            return jsonify({'message': 'Invalid id task'}), 404

        return jsonify({
            'id': video.id,
            'description': video.description,
            'status': VideoStatus(video.status).value,
            'date': video.timestamp,
            'path': video.path
        }), 200
