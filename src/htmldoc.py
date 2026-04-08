import re
import os

from htmltree import HTMLTree

class HTMLDoc:
    def __init__(self, path:str, contents:HTMLTree):
        self.path = path
        self.contents = contents
        self.title = contents.extract_title()
        if self.title is None:
            raise ValueError("Title not found")

    def write_doc(self, template_path:str):
        template = open(template_path).read()
        #print(template)
        with open(self.path, mode="w") as f:
            if isinstance(self.contents, HTMLTree):
                text = self.contents.root.to_html()
            else:
                text = self.contents
            template = re.sub(r"\{\{ Title \}\}", self.title, template)
            template = re.sub(r"\{\{ Content \}\}", text, template)    
            f.write(template)
            f.close()
