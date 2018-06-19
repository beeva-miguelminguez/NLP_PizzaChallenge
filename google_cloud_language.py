# buildin
import os
import sys
import json

# vendor
import requests
from flask import Blueprint, request
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# assets
from config import Config

credentials = Config("config/credentials.cfg")
if credentials.get("google", "CREDENTIALS"):
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials.get("google", "CREDENTIALS")
else:
	sys.exit("No Google CREDENTIALS")

google_cloud_language_blueprint = Blueprint("google-cloud-language", __name__)
client = language.LanguageServiceClient()


###############################
# GOOGLE CLOUD LANGUAGE INDEX #
###############################
@google_cloud_language_blueprint.route("/")
def index():
	return json.dumps({
		"sentiment analysis": "/google-cloud-language/sentiment",
		"entities extraction": "/google-cloud-language/entities",
		"part of speech analysis": "/google-cloud-language/part-of-speech",
		"categories classification": "/google-cloud-language/categories",
	})


######################
# SENTIMENT ANALYSIS #
######################
@google_cloud_language_blueprint.route("/sentiment", methods=[ "POST" ])
def sentiment():
	content = request.form.get("content")
	if content:
		try:
			document = types.Document(content=content, type=enums.Document.Type.PLAIN_TEXT)
			response = client.analyze_sentiment(document)
			sentiment = response.document_sentiment
			return json.dumps({
				"magnitude": sentiment.magnitude,
				"score": sentiment.score
			})
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400


######################
# ENTITES EXTRACTION #
######################
@google_cloud_language_blueprint.route("/entities", methods=[ "POST" ])
def entities():
	content = request.form.get("content")
	if content:
		try:
			document = types.Document(content=content, type=enums.Document.Type.PLAIN_TEXT)
			response = client.analyze_entities(document)
			entities = []
			for e in response.entities:
				entity = {
					"name": e.name,
					"type": e.type,
					"salience": e.salience
				}
				if e.metadata:
					entity["metadata"] = {
						"key": e.metadata.get("key"),
						"value": e.metadata.get("value")
					}
				entities.append(entity)
			return json.dumps(entities)
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400


###########################
# PART-OF-SPEECH ANALYSIS #
###########################
@google_cloud_language_blueprint.route("/part-of-speech", methods=[ "POST" ])
def partofspeech():
	content = request.form.get("content")
	if content:
		try:
			document = types.Document(content=content, type=enums.Document.Type.PLAIN_TEXT)
			response = client.analyze_syntax(document)
			tokens = []

			pos_tags = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
						'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
			for t in response.tokens:
				tokens.append({
					"tag": pos_tags[t.part_of_speech.tag],
					"token": t.text.content
				})
			return json.dumps(tokens)
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400


#######################
# TEXT CLASSIFICATION #
#######################
@google_cloud_language_blueprint.route("/categories", methods=[ "POST" ])
def categories():
	content = request.form.get("content")
	if content:
		try:
			document = types.Document(content=content, type=enums.Document.Type.PLAIN_TEXT)
			response = client.classify_text(document)
			candidates = []
			for c in response.categories:
				candidates.append({
					"name": c.name,
					"confidence": c.confidence
				})
			return json.dumps(candidates)
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500

	return "Bad request: 'content' (multipart/form-data) required.", 400