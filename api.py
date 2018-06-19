import json
from flask import Flask
from flask_cors import CORS

from rosette import rosette_blueprint

app = Flask(__name__)
app.register_blueprint(rosette_blueprint, url_prefix='/rosette')
CORS(app)

@app.route("/")
def index():
	return json.dumps({
		"Rosette Text Analytics": "/rosette"
	})

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)