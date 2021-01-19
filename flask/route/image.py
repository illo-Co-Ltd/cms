from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, request, jsonify, current_app

from model.db_base import db as db
from model.user_model import User
from model.company_model import Company
from model.target_model import Target
from model.device_model import Device
from model.project_model import Project
from model.image_model import Image

from util.logger import logger
from util.auth_util import token_required

import jwt
import datetime

image_route = Blueprint('image_route', __name__)

