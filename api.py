# -*- coding: utf-8 -*-
import os
import json
from flask import Flask
from flask_cors import CORS

from rosette import rosette_blueprint
from interpretext import interpretext_blueprint
from google_cloud_language import google_blueprint
from azure_text_analytics import azure_blueprint
#from twitter_service import twitter_blueprint

app = Flask(__name__)
app.register_blueprint(rosette_blueprint, url_prefix="/rosette")
app.register_blueprint(interpretext_blueprint, url_prefix="/interpretext")
app.register_blueprint(google_blueprint, url_prefix="/google")
app.register_blueprint(azure_blueprint, url_prefix="/azure")
#app.register_blueprint(twitter_blueprint, url_prefix="/twitter")
CORS(app)


@app.route("/")
def index():
	return json.dumps({
		"Rosette Text Analytics": "/rosette",
		"Google Cloud Natural Language": "/google",
		"Azure Text Analytics": "/azure",
		"Interpretext API": "/interpretext",
		"Twitter threads extraction": "/twitter"
	})


if __name__ == "__main__":
	port = os.environ.get("PORT", 80)
	app.run(host="0.0.0.0", port=int(port))
