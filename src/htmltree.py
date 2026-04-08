import converter

from htmlnode import HTMLNode, ParentNode
from markdowndoc import MarkdownDoc

class HTMLTree:
    def __init__(self, root:ParentNode):
        self.root = root

    @classmethod
    def from_markdown_doc(cls, doc:MarkdownDoc|str):
        if isinstance(doc, MarkdownDoc):
            doc = doc.contents
        block_nodes = converter.markdown_to_html_nodes(doc)
        div = ParentNode("div", block_nodes)
        #print(div.to_html())
        return HTMLTree(div)
    
    def extract_title(self):
        assert self.root.children is not None
        for child in self.root.children:
            if child.tag == "h1":
                title = ""
                for granchild in child.children:
                    title += granchild.value
            return title        
        raise Exception("No top tier heading detected, title could not be parsed")
    
