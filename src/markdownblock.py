from enum import Enum

#Supported types of markdown blocks we store/parse
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

#Structure to store markdown block info
class MarkdownBlock:
    def __init__(self, text:str, block_type:BlockType):
        self.text = text
        self.block_type = block_type

    def __eq__(self, other):
        if not isinstance(other, MarkdownBlock):
            return False
        return True if self.text == other.text and self.block_type == other.block_type else False

    def __repr__(self):
        return f"\n({self.text}, {self.block_type})\n"