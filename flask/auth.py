import logging

from flask import Blueprint, make_response

_logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    _logger.info('Login route called....')
    return make_response({
        'status': 'success',
        'message': 'Login route called....',
    })
