from IModel import IModel
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import storage
from google.cloud import language
from google.cloud import translate
from google.cloud.language import enums
from google.cloud.language import types
import six
import os
import sys
import json
import urllib


class AppModel(IModel):
    def __init__(self,app):
        self.arg = app
        self.CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')

    """
		Finds labels for the photo passed in
		@params: photo is the image to check, use photo = request.files['file']
		Returns a tuple containing an array of labels and the uri to the image
    """
    def labelImage(self,photo):
    	# Create a Cloud Storage client
    	storage_client = storage.Client()
    	# Get the bucket
    	bucket = storage_client.get_bucket(self.CLOUD_STORAGE_BUCKET)
    	# Make a blob and upload the file's content
    	blob = bucket.blob(photo.filename)
    	blob.upload_from_string(photo.read(),content_type=photo.content_type)
    	blob.make_public()

    	# Instantiate a client
    	client = vision.ImageAnnotatorClient()
    	# load image
    	source_uri = 'gs://{}/{}'.format(self.CLOUD_STORAGE_BUCKET, blob.name)
    	image = vision.types.Image(source=vision.types.ImageSource(gcs_image_uri=source_uri))

    	# Perform label detection on the image
    	response = client.label_detection(image=image)
    	labels = response.label_annotations
    	# Returns the labels detected in the image
    	return (labels,blob.public_url)

    """
        Sends query to google knowledge graph
        @params: label is a string that is sent
        Returns a description of the first search result obtained.
    """
    def knowledgeGraph(self, label):
        api_key = open('.api_key').read()
        query = label
        service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
        params = {
                'query': query,
                'limit': 1,
                'indent': True,
                'key': api_key,
        }
        url = service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())
        return response['itemListElement'][0]['result']['detailedDescription']['articleBody']

    """
        Asks google language to analyze the sentiment
        @params: text is the string to analyze
        Returns a value from -1 to 1, which corresponds to how positive text is.
    """
    def sentiment_text(self, text):
        client = language.LanguageServiceClient()
        
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')
        document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document).document_sentiment
        feeling = sentiment.score
        return (feeling)
	
    """
        Takes in a target language and a text to translate
        using google.cloud translate API
        
        Returns the translated string in the target language
	    
    """
    def translate_text(self, target, text):
	    translate_client = translate.Client()
	    
	    if isinstance(text, six.binary_type):
	        text = text.decode('utf-8')
	    
	    result = translate_client.translate(
	        text, target_language=target)
	    
	    return result['translatedText']
