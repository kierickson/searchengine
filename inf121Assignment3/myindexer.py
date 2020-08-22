#tfidf
#fields
class Posting:
    def __init__(self, docid, frequency, positions):
        self.docid = docid
        #self.tfidf = tfidf
        self.frequency = frequency
        #self.fields = fields
        self.positions = positions


    def __repr__(self):
        return "DOC_ID: " + str(self.docid) + " (freq: " + str(self.frequency) + ") (positions:  " + str(self.positions) + ") "
