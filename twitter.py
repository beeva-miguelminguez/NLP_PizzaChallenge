# -*- coding: utf-8 -*-
# vendor
import tweepy

# assets
from config import Config


class TwitterUtil:
	def __init__(self):
		credentials = Config("config/credentials.cfg")
		self.api = None
		self.credentials = {
			"CONSUMER_KEY": credentials.get('twitter', 'CONSUMER_KEY'),
			"CONSUMER_SECRET": credentials.get('twitter', 'CONSUMER_SECRET'),
			"ACCESS_TOKEN": credentials.get('twitter', 'ACCESS_TOKEN'),
			"ACCESS_TOKEN_SECRET": credentials.get('twitter', 'ACCESS_TOKEN_SECRET')
		}

		self.authenticate()

	def authenticate(self):
		auth = tweepy.OAuthHandler(self.credentials["CONSUMER_KEY"], self.credentials["CONSUMER_SECRET"])
		auth.set_access_token(self.credentials["ACCESS_TOKEN"], self.credentials["ACCESS_TOKEN_SECRET"])
		self.api = tweepy.API(auth, wait_on_rate_limit=True)

	def find_reply_to_tweet(self, tweet, tweets):
		for item in tweets:
			if item.in_reply_to_status_id is not None and item.in_reply_to_status_id == tweet.id:
				return item

	def fetch_all_replies(self, reply, tweets):
		replies = [reply]
		depht_of_search = 0
		while depht_of_search >= 0:
			parent = replies[depht_of_search]
			child = self.find_reply_to_tweet(parent, tweets)
			if child is None:
				depht_of_search = -1
			else:
				replies.append(child)
				depht_of_search += 1
		return replies

	def get_hashtag_tweets(self, hashtag):
		try:
			query = hashtag if hashtag.startswith("#") else "#{hashtag}".format(hashtag=hashtag)
			status = self.api.search(q=query, count=200, tweet_mode='extended')
			return list(map(lambda s: {
				"date": s.created_at.isoformat(),
				"text": s.full_text,
				"user": "{user} (@{alias})".format(user=s.user.name, alias=s.user.screen_name)
			}, status))
		except Exception as e:
			print(e)
			raise e

	def get_user_tweets(self, username, count=300):
		try:
			status = self.api.user_timeline(screen_name=username, count=count, tweet_mode='extended')
			return list(map(lambda s: {
				"date": s.created_at.isoformat(),
				"text": s.full_text
			}, status))
		except Exception as e:
			print(e)
			raise e

	def get_user_threads(self, username, count=300):
		try:
			status = self.api.user_timeline(screen_name=username, count=count, tweet_mode='extended')
			# Let's fetch all the tweets
			tweets = [s for s in status]
			# Let's filter to the main tweets that may be heads in a thread
			if len(tweets) > 0:
				main_twits = list(filter(lambda x: x._json.get("in_reply_to_status_id") is None, tweets))

				# Now we get all the threads that have a reply, forming head:status, replies[status] object
				timeline_threads = []
				for twit in main_twits:
					reply = self.find_reply_to_tweet(twit, tweets)
					if reply is not None:
						new_thread = {'head': twit, 'replies': [reply]}
						timeline_threads.append(new_thread)

				# Now we try to find the other replies
				for thread in timeline_threads:
					thread['replies'] = self.fetch_all_replies(thread.get('replies')[0], tweets)
				return timeline_threads
			return []
		except Exception as e:
			print(e)
			raise e

	def format_threads(self, threads):
		threads_formated = []
		for thread in threads:
			new_thread = [thread.get('head').full_text]
			for reply in thread.get('replies'):
				new_thread.append(reply.full_text)
			threads_formated.append(new_thread)
		return threads_formated
