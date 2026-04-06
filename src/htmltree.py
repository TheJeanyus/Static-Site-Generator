import src.converter as converter

from src.htmlnode import HTMLNode, ParentNode
from src.markdowndoc import MarkdownDoc

class HTMLTree:
    def __init__(self, root:HTMLNode):
        self.root = root

    @classmethod
    def from_markdown_doc(cls, doc:MarkdownDoc|str):
        if isinstance(doc, MarkdownDoc):
            doc = doc.contents
        block_nodes = converter.markdown_to_html_nodes(doc)
        div = ParentNode("div", block_nodes)
        #print(div.to_html())
        return HTMLTree(div)
    
