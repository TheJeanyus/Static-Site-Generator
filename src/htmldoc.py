import sys
import os

from htmltree import HTMLTree

class HTMLDoc:
    def __init__(self, path, title, contents):
        self.path = path
        self.title = title
        self.contents = contents

    def write_doc(self):
        with os.open() as f:
            f.write()