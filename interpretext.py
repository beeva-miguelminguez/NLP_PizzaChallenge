# -*- coding: utf-8 -*-
# buildin
import json

# vendor
import requests
from flask import Blueprint
from flask import request


interpretext_blueprint = Blueprint("interpretext", __name__)
INTERPRETEXT_URI = "http://interpretext/{action}"


######################
# INTERPRETEXT INDEX #
######################
@interpretext_blueprint.route("/")
def index():
	return json.dumps({
		"language detection": "/interpretext/language",
		"tokens extraction": "/interpretext/tokenize",
		"part of speech analysis": "/interpretext/part-of-speech",
		"summary extraction": "/interpretext/summary",
	})


######################
# LANGUAGE DETECTION #
######################
@interpretext_blueprint.route("/language", methods=[ "POST" ])
def language():
	if request.form.get("content"):
		try:
			data = {
				"input": request.form.get("content")
			}
			res = requests.post(INTERPRETEXT_URI.format(action="language"), data=data)
			return json.dumps(res.json())
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400


######################
# ENTITES EXTRACTION #
######################
@interpretext_blueprint.route("/entities", methods=[ "POST" ])
def tokenize():
	if request.form.get("content"):
		try:
			data = {
				"input": request.form.get("content")
			}
			res = requests.post(INTERPRETEXT_URI.format(action="tokenize"), data=data)
			return json.dumps(res.json())
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400


######################
# SENTIMENT ANALYSIS #
######################
@interpretext_blueprint.route("/sentiment", methods=[ "POST" ])
def partofspeech():
	if request.form.get("content"):
		try:
			data = {
				"input": request.form.get("content")
			}
			res = requests.post(INTERPRETEXT_URI.format(action="postagging"), data=data)
			return json.dumps(res.json())
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400


####################
# TOPIC EXTRACTION #
####################
@interpretext_blueprint.route("/topics", methods=[ "POST" ])
def summary():
	if request.form.get("content"):
		try:
			data = {
				"input": request.form.get("content")
			}
			res = requests.post(INTERPRETEXT_URI.format(action="summary"), data=data)
			return json.dumps(res.json())
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400
