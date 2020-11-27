from flask import Blueprint

blueprint = Blueprint(
    'kgraph_blueprint',
    __name__,
    url_prefix='/kgraph',
    template_folder='templates',
    static_folder='static'
)
