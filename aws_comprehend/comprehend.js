class Comprehend {
	constructor() {
		AWS.config.region = 'eu-west-1';
		AWS.config.apiVersion = { comprehend: '2017-11-27' };
		AWS.config.credentials = new AWS.CognitoIdentityCredentials({
			IdentityPoolId: 'eu-west-1:fe4b9a03-cb9f-460a-8f29-91e82714ac90'
		});

		this.comprehend = new AWS.Comprehend();
	}

	language(Text, callback) {
		return new Promise((resolve, reject) => {
			this.comprehend.detectDominantLanguage({ Text }, (err, data) => {
				if (err) reject(err);
				else resolve(data);
			});	
		});
	}

	entities(Text, LanguageCode, callback) {
		return new Promise((resolve, reject) => {
			this.comprehend.detectEntities({ Text, LanguageCode }, (err, data) => {
				if (err) reject(err);
				else resolve(data);
			});	
		});
	}

	keyphrases(Text, LanguageCode, callback) {
		return new Promise((resolve, reject) => {
			this.comprehend.detectKeyPhrases({ Text, LanguageCode }, (err, data) => {
				if (err) reject(err);
				else resolve(data);
			});	
		});
	}

	sentiment(Text, LanguageCode, callback) {
		return new Promise((resolve, reject) => {
			this.comprehend.detectSentiment({ Text, LanguageCode }, (err, data) => {
				if (err) reject(err);
				else resolve(data);
			});	
		});
	}
}