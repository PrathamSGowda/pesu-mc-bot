from flask import Flask
<<<<<<< HEAD

app = Flask(__name__)

=======
import logging

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s: %(message)s'
)
>>>>>>> 3716ca6 (uv migration and multi-threading support)

@app.route("/")
def home():
    return "[HOST] Bot is online"

<<<<<<< HEAD

def run_webserver():
    app.run(host="0.0.0.0", port=7860)
=======
@app.route("/health")
def health():
    return {"status": "healthy"}, 200
>>>>>>> 3716ca6 (uv migration and multi-threading support)
