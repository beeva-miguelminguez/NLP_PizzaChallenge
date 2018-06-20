# -*- coding: utf-8 -*-
# buildin
import os
import sys
import json

# vendor
import requests
from flask import Blueprint
from flask import request

# assets
from config import Config

azure_blueprint = Blueprint("azure", __name__)
credentials = Config("config/credentials.cfg")
KEY = credentials.get("azure", "KEY")
if not KEY:
	sys.exit("No Azure KEY")

AZURE_URI = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/{action}"
HEADERS = {
	"Ocp-Apim-Subscription-Key": KEY,
	"Content-Type": "application/json"
}


##############################
# AZURE TEXT ANALYTICS INDEX #
##############################
@azure_blueprint.route("/")
def index():
	return json.dumps({
		"language detection": "/azure/language",
		"entities extraction": "/azure/entities",
		"part of speech analysis": "/azure/sentiment",
		"categories classification": "/azure/topics",
	})


######################
# LANGUAGE DETECTION #
######################
@azure_blueprint.route("/language", methods=[ "POST" ])
def language():
	if request.form.get("content"):
		try:
			data = json.dumps({
				"documents": [ { "id": 1, "text": request.form.get("content") } ]
			})
			res = requests.post(AZURE_URI.format(action="languages"), headers=HEADERS, data=data)
			return json.dumps(res.json())
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400


######################
# ENTITES EXTRACTION #
######################
@azure_blueprint.route("/entities", methods=[ "POST" ])
def entities():
	if request.form.get("content"):
		try:
			data = json.dumps({
				"documents": [ { "id": 1, "text": request.form.get("content") } ]
			})
			res = requests.post(AZURE_URI.format(action="entities"), headers=HEADERS, data=data)
			return json.dumps(res.json())
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400


######################
# SENTIMENT ANALYSIS #
######################
@azure_blueprint.route("/sentiment", methods=[ "POST" ])
def sentiment():
	if request.form.get("content"):
		try:
			data = json.dumps({
				"documents": [ { "id": 1, "text": request.form.get("content") } ]
			})
			res = requests.post(AZURE_URI.format(action="sentiment"), headers=HEADERS, data=data)
			return json.dumps(res.json())
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400


####################
# TOPIC EXTRACTION #
####################
@azure_blueprint.route("/topics", methods=[ "POST" ])
def topics():
	if request.form.get("content"):
		try:
			data = json.dumps({
				"documents": [ { "id": 1, "text": request.form.get("content") } ]
			})
			res = requests.post(AZURE_URI.format(action="keyPhrases"), headers=HEADERS, data=data)
			return json.dumps(res.json())
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400

