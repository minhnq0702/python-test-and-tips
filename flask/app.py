import logging

# from . import auth
import auth

from flask import Blueprint, Flask

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
_logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(auth.bp)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=3000)
    from waitress import serve
    serve(app, host="0.0.0.0", port=3000)
