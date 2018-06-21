# -*- coding: utf-8 -*-
# buildin
import json


# vendor
from flask import request
from flask import Blueprint
from twitter import TwitterUtil

twitter_blueprint = Blueprint("twitter", __name__)


@twitter_blueprint.route("/")
def index():
	return json.dumps({
		"User timeline tweets": "/twitter/tweets",
		"Hashtag tweets": "/twitter/hashtag",
		"User timeline threads": "/twitter/threads"
	})


@twitter_blueprint.route("/tweets", methods=["POST"])
def tweets():
	if request.form.get("username"):
		username = request.form.get("username")
		try:
			tu = TwitterUtil()
			tweets = tu.get_user_tweets(username)
			return json.dumps(tweets)
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500
	else:
		return "Bad request: 'username' (multipart/form-data) required.", 400


@twitter_blueprint.route("/hashtag", methods=["POST"])
def hashtag():
	if request.form.get("hashtag"):
		hashtag = request.form.get("hashtag")
		try:
			tu = TwitterUtil()
			tweets = tu.get_hashtag_tweets(hashtag)
			return json.dumps(tweets)
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500
	else:
		return "Bad request: 'hashtag' (multipart/form-data) required.", 400


@twitter_blueprint.route("/threads", methods=["POST"])
def threads():
	if request.form.get("username"):
		username = request.form.get("username")
		try:
			tu = TwitterUtil()
			tweets = tu.get_user_threads(username)
			formated = tu.format_threads(tweets)
			return json.dumps(formated)
		except Exception as e:
			print(e)
			return "Internal server error: %s" % str(e), 500
	else:
		return "Bad request: 'username' (multipart/form-data) required.", 400