from flask import Blueprint, request, jsonify, current_app
from util.logger import logger
from model import user_model
from model import device_model
from util.auth_util import token_required

import jwt
import datetime

device_route = Blueprint('device_route', __name__)


@device_route.route('/tweet', methods=["GET"])
@token_required
def tweet_list(current_user):
    logger.info("get Tweet List")
    tweet_list = device_model.Tweet.query.all()
    return jsonify([t.to_dict() for t in tweet_list])


@device_route.route('/tweet', methods=["POST"])
@token_required
def create_tweet(current_user):
    logger.info("Tweet Post!")
    try:
        data = request.get_json()
        title = data.get("title")
        words = data.get("words")
        created_at = datetime.datetime.utcnow()
        updated_at = datetime.datetime.utcnow()

        db = device_model.db
        tweet = device_model.Tweet(
            title=title,
            words=words,
            creator=current_user.username,
            created_at=created_at,
            updated_at=updated_at
        )
        db.session.add(tweet)
        db.session.commit()
        return jsonify(tweet.to_dict()), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'fail to save tweet'}), 200
