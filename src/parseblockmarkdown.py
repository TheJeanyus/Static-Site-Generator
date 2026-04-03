import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class MarkdownBlock:
    BLOCK_REGEX = regex_test = r"(?P<heading>#+\x20.*)|(?P<code>```\n[^`]*\n```)|(?P<quote>(?:^>\x20?.*\n)*)|"\
        r"(?P<unordered_list>(?:^-\x20.*\n)*)|(?P<ordered_list>(?:^\d\.\x20.*\n)*)|(?P<paragraph>^\n([^#`>\-\d](?:.+\n)*))"
    BLOCK_PATTTERN = re.compile(BLOCK_REGEX, flags=re.MULTILINE)
    
    def __init__(self, text:str, block_type:BlockType):
        self.text = text
        self.block_type = block_type

    def __eq__(self, other):
        if not isinstance(other, MarkdownBlock):
            return False
        return True if self.text == other.text and self.block_type == other.block_type else False

    def __repr__(self):
        return f"\n({self.text}, {self.block_type})\n"
    
def markdown_to_blocks(markdown):
    m = re.finditer(MarkdownBlock.BLOCK_PATTTERN, markdown)
    full_list = [x.groupdict() for x in m if x.group() != ""]
    block_list:list[MarkdownBlock] = []
    for block_dict in full_list:
        for key in block_dict:
            if block_dict[key] is not None and block_dict[key].strip() != "":
                block_list.append(MarkdownBlock(block_dict[key].strip(), BlockType(key)))
    #print(block_list)
    return block_list
        

# def markdown_to_blocks(markdown):
#     blocks = [block.strip() for block in markdown.split("\n\n")]
#     blocks = [block for block in blocks if block != ""]
#     return blocks

# def block_to_block_type(block:str):
#     # 1:Heading, 2:Code, 3:Quote, 4:Ulist, 5:OList
#     regex_test = r"(?P<heading>#.*)|(?P<code>```\n.*\n```)|(?P<quote>(?:^>.*\n)*)|"\
#         r"(?P<ulist>(?:^-.*\n)*)|(?P<olist>(?:^\d\..*\n)*)|(?P<paragraph>(?:.*\n)*)"
#     blocks = re.match(regex_test,block).group(1,2,3,4,5)
#     block_type_index = 0
#     for ind, item in enumerate(blocks):
#         if item != "":
#             block_type_index = ind + 1
#     block_types = [BlockType.PARAGRAPH, BlockType.HEADING,BlockType.CODE, BlockType.QUOTE, 
#                    BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]
#     return block_types[block_type_index]
