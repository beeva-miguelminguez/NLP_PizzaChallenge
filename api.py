# -*- coding: utf-8 -*-
import os
import json
from flask import Flask
from flask import request
from flask_cors import CORS

from twitter_threads import TwitterUtil
from rosette import rosette_blueprint
from interpretext import interpretext_blueprint
from google_cloud_language import google_blueprint
from azure_text_analytics import azure_blueprint


app = Flask(__name__)
app.register_blueprint(rosette_blueprint, url_prefix="/rosette")
app.register_blueprint(interpretext_blueprint, url_prefix="/interpretext")
app.register_blueprint(google_blueprint, url_prefix="/google")
app.register_blueprint(azure_blueprint, url_prefix="/azure")
CORS(app)


@app.route("/")
def index():
	return json.dumps({
		"Rosette Text Analytics": "/rosette",
		"Google Cloud Natural Language": "/google",
		"Azure Text Analytics": "/azure",
		"Twitter threads extraction": "/twitter"
	})


@app.route("/twitter", methods=[ "POST" ])
def twitter():
	if request.form.get("username"):
		username = request.form.get("username")
		try:
			tu = TwitterUtil()
			threads = tu.get_user_tweets(username)
			formated_threads = tu.format_threads(threads)
			return json.dumps(formated_threads)
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500
	else:
		return "Bad request: 'username' (multipart/form-data) required.", 400


if __name__ == "__main__":
	port = os.environ.get("PORT", 80)
	app.run(host="0.0.0.0", port=int(port), debug=True)
