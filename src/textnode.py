from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "Italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
        
class TextNode:
    def __init__(self, text :str, text_type :TextType, url :str|None =None):
        if not isinstance(text_type, TextType):
            raise TypeError("text_type is not a valid entry, see TextType declaration")
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, value):
        if not isinstance(value, TextNode):
            return False
        elif self.text == value.text and self.text_type == value.text_type and self.url == value.url:
            return True
        else:
            return False
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def text_node_to_html_node(self):
        props = None
        value = self.text
        match self.text_type:
            case TextType.TEXT:
                tag = None
            case TextType.BOLD:
                tag = "b"
            case TextType.ITALIC:
                tag = "i"
            case TextType.CODE:
                tag = "code"
            case TextType.LINK:
                tag = "a"
                props = {"href":self.url}
            case TextType.IMAGE:
                tag = "img"
                value = None
                props = {"src":self.url, "alt":self.text}
        return LeafNode(tag, value, props)