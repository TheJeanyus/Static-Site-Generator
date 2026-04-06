import converter

from htmlnode import HTMLNode, ParentNode
from markdowndoc import MarkdownDoc

class HTMLTree:
    def __init__(self, root:HTMLNode):
        self.root = root

    @classmethod
    def from_markdown_doc(cls, doc:MarkdownDoc|str):
        if isinstance(doc, MarkdownDoc):
            doc = doc.contents
        block_nodes = converter.markdown_to_html_nodes(doc)
        div = ParentNode("div", block_nodes)
        return HTMLTree(div)
    
