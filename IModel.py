from abc import ABCMeta, abstractmethod


class IModel:
    __metaclass__ = ABCMeta

    """
        Finds labels for the photo passed in
        @params: photo is the image to check, use photo = request.files['file']
        Returns a tuple containing an array of labels and the uri to the image
    """

    def labelImage(self, photo):
        pass

    """
        Sends query to google knowledge graph
        @params: label is a string that is sent
        Returns a description of the first search result obtained.
    """

    def knowledgeGraph(self, label):
        pass

    """
        Asks google language to analyze the sentiment
        @params: text is the string to analyze
        Returns a value from -1 to 1, which corresponds to how positive text is.
    """

    def sentiment_text(self, text):
        pass
