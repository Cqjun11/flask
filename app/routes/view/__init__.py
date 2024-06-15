# coding=utf-8
from flask import Blueprint

bp = Blueprint('view', __name__)

from app.routes.view import device_view


