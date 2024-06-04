# coding=utf-8

from flask import render_template
from app.routes.error import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('/error/404.html'), 404



