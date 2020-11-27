from flask import Blueprint

blueprint = Blueprint(
    'HR_content_blueprint',
    __name__,
    url_prefix='/HR_content',
    template_folder='templates',
    static_folder='static'
)