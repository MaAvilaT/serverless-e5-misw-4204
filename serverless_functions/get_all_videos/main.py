import functions_framework
from flask import jsonify

from library_serverless_core.persistence.database import open_session
from library_serverless_core.security.token_utils import verify_token, decode_token
from library_serverless_core.shared_models.Video import Video, VideoStatus


@functions_framework.http
def get_all_videos(request):
    if request.method != 'GET':
        return jsonify(''), 404

    if not verify_token(request):
        return jsonify(''), 505

    user_id = decode_token(request)['user_id']

    order = request.args.get('order')
    lim = request.args.get('max')

    with open_session() as session:
        if order == '0':
            videos = session.query(Video).filter(Video.user_id == user_id).order_by(Video.id.asc()).limit(lim).all()
        elif order == '1':
            videos = session.query(Video).filter(Video.user_id == user_id).order_by(Video.id.desc()).limit(lim).all()
        else:
            response = jsonify({'message': 'Invalid value for order'})
            return response, 401

        videos_dict = [{
            'id': video.id,
            'description': video.description,
            'status': VideoStatus(video.status).value,
            'date': video.timestamp
        } for video in videos]

        return jsonify(videos_dict), 200
