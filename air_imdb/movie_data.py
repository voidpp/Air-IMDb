import json
import os

class MovieMap(object):
    def __init__(self, cache_file):
        self.filename = cache_file
        self.data = {}
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename) as f:
                self.data = json.load(f)
        except:
            pass

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)
