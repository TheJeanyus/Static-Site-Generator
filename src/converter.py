import re

from src.textnode import TextType, TextNode
from src.markdowndoc import MarkdownDoc
from src.markdownblock import BlockType, MarkdownBlock
from src.htmlnode import ParentNode, LeafNode


#Helper for conversion that are one-to-many or many-to-many

#Regex Patterns used in the module
BLOCK_PATTTERN = re.compile(r"(?P<heading>#+\x20.*)|"\
                    r"(?P<code>```\n[^`]*\n```)|"\
                    r"(?P<quote>(?:^>\x20?.*\n)*)|"\
                    r"(?P<unordered_list>(?:^-\x20.*\n)*)|"\
                    r"(?P<ordered_list>(?:^\d\.\x20.*\n)*)|"\
                    r"(?P<paragraph>^\n([^#`>\-\d](?:.+\n)*))", 
                    flags=re.MULTILINE)

IMAGE_PATTERN = re.compile(r"(!\[.*?\]\(.+?\))")

LINK_PATTERN = re.compile(r"(?<!\!)(\[.+?\]\(.+?\))")

#Dictionary mapping inline delimiters to appropriate tags
DELIMITER_MAP = {
                "**":TextType.BOLD,
                "_":TextType.ITALIC,
                "`":TextType.CODE
                }

#Process markdown doc contents to html nodes
def markdown_to_html_nodes(doc:str|MarkdownDoc):
    if isinstance(doc, MarkdownDoc):
        doc = doc.contents
    block_list = markdown_to_blocks(doc)
    block_nodes:list[ParentNode] = []
    for block in block_list:
        match block.block_type:
            case BlockType.PARAGRAPH:
                block_node = parse_paragraph(block.text)
            case BlockType.HEADING:
                block_node = parse_heading(block.text)
            case BlockType.CODE:
                block_node = parse_code(block.text)
            case BlockType.QUOTE:
                block_node = parse_quote(block.text)
            case BlockType.UNORDERED_LIST:
                block_node = parse_list(block.text, False)
            case BlockType.ORDERED_LIST:
                block_node = parse_list(block.text, True)
        block_nodes.append(block_node)
    return block_nodes

#Helper to split doc contents into parseable blocks
def markdown_to_blocks(doc:str|MarkdownDoc):
    if isinstance(doc, MarkdownDoc):
        doc = doc.contents
    m = re.finditer(BLOCK_PATTTERN, doc)
    full_list = [x.groupdict() for x in m if x.group() != ""]
    block_list:list[MarkdownBlock] = []
    for block_dict in full_list:
        for key in block_dict:
            if block_dict[key] is not None and block_dict[key].strip() != "":
                block_list.append(MarkdownBlock(block_dict[key].strip(), BlockType(key)))
    #print(block_list)
    return block_list

#Helpers to parse markdown block types
def parse_paragraph(text:str):
    text = " ".join(text.split("\n")).strip(" ")
    inline_elements = [node.text_node_to_html_node() for node in parse_text([TextNode(text, TextType.TEXT)])]
    return ParentNode("p", inline_elements)

def parse_heading(text:str):
    start = re.match(r"^#+ ", text)
    if start:
        start_len = len(start.group()) - 1
    else:
        raise Exception("Markdown heading parsing failed, invalid format detected")
    inline_elements = [node.text_node_to_html_node() for node in parse_text([TextNode(text[start_len:], TextType.TEXT)])]
    return ParentNode(f"h{start_len}", inline_elements)

def parse_code(text:str):
    return ParentNode("pre",[ParentNode("code",[LeafNode(None, text[4:-3])])])

def parse_quote(text:str):
    quote = "\n".join([line[1:].strip(" ") for line in text.split("\n")])
    print(quote)
    return ParentNode("blockquote", markdown_to_html_nodes(quote))

def parse_list(text:str, ordered:bool):
    lines = text.split("\n")
    line_nodes = []
    for line in lines:
        m = re.match(r"^(?:- |\d\. )(.*)", line, flags=re.MULTILINE)
        if m:
            line = m.group(1)
        else:
            raise Exception("Markdown list parsing failed, invalid format detected")
        line_items = [node.text_node_to_html_node() for node in parse_text([TextNode(line, TextType.TEXT)])]
        line_node = ParentNode("li", line_items)
        line_nodes.append(line_node)
    return ParentNode("ol" if ordered else "ul", line_nodes)

#Functions to handle inline parsing to text nodes
def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str):
    if delimiter not in DELIMITER_MAP:
        raise Exception("Unknown delimiter provided, cannot correctly type children")
    text_type = DELIMITER_MAP[delimiter]
    new_nodes:list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        node_pieces = old_node.text.split(delimiter)
        if len(node_pieces) % 2 != 1:
            raise Exception(f"An uneven number of delimters was found in: {old_node.text}")
        new_nodes.extend(
            [TextNode(text, text_type if index % 2 else TextType.TEXT) 
            for index, text in enumerate(node_pieces)]
            )
    new_nodes = [node for node in new_nodes if node.text != ""]
    return new_nodes

def split_nodes_images(old_nodes:list[TextNode]):
    new_nodes:list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = list(filter(None,re.split(IMAGE_PATTERN,old_node.text)))
        for i in range(len(matches)):
            if re.match(IMAGE_PATTERN, matches[i]):
                halves = matches[i].split("](")
                new_nodes.append(TextNode(halves[0][2:], TextType.IMAGE, halves[1][:-1]))
            else:
                new_nodes.append(TextNode(matches[i], TextType.TEXT))
    return new_nodes

def split_nodes_links(old_nodes:list[TextNode]):
    new_nodes:list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = list(filter(None,re.split(LINK_PATTERN,old_node.text)))
        for i in range(len(matches)):
            if re.match(LINK_PATTERN, matches[i]):
                halves = matches[i].split("](")
                new_nodes.append(TextNode(halves[0][1:], TextType.LINK, halves[1][:-1]))
            else:
                new_nodes.append(TextNode(matches[i], TextType.TEXT))
    return new_nodes

def parse_text(old_nodes:list[TextNode]):
    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_images(
                    split_nodes_links(
                        old_nodes
                    )
                )
            , "_")
        , "`"), 
    "**")        
