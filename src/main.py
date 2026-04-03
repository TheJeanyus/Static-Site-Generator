import re

from parseblockmarkdown import BlockType, markdown_to_blocks
from parseinlinemarkdown import parse_text
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

def main():
    
    pass

def div_wrap(nodes:list[HTMLNode]):
    return ParentNode("div", nodes)

def markdown_to_html_node(markdown:str):
    block_list = markdown_to_blocks(markdown)
    block_nodes = []
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

def parse_paragraph(text:str):
    text = " ".join(text.split("\n")).strip(" ")
    inline_elements = parse_text([TextNode(text, TextType.TEXT).text_node_to_html_node()])
    return ParentNode("p", inline_elements)

def parse_heading(text:str):
    start = re.match(r"^#+ ", text)
    if start:
        start_len = len(start.group()) - 1
    else:
        raise Exception("Markdown heading parsing failed, invalid format detected")
    inline_elements = [node.text_node_to_html_node() for node in parse_text(text[start_len:])]
    return ParentNode(f"h{start_len}", inline_elements)

def parse_code(text:str):
    return ParentNode("pre",[ParentNode("code",[LeafNode("", text)])])

def parse_quote(text:str):
    quote = "\n".join([line[1:].strip(" ") for line in text.split("\n")])
    return ParentNode("blockquote", markdown_to_html_node(quote))

def parse_list(text:str, ordered:bool):
    lines = text.split("\n")
    line_nodes = []
    for line in lines:
        m = re.match(r"^(?:- |\d\. )(.*)", line, flags=re.MULTILINE)
        if m:
            line = m.group(1)
        else:
            raise Exception("Markdown list parsing failed, invalid format detected")
        line_items = [node.text_node_to_html_node() for node in parse_text(line)]
        line_node = ParentNode("li", line_items)
        line_nodes.append(line_node)
    return ParentNode("ol" if ordered else "ul", line_nodes)

if __name__ == "__main__":
    main()

#heading        ->      <h1> to <h6>
#paragraph      ->      <p>
#code           ->      <pre><code>
#quote          ->      <blockquote>
#unordered_list ->      <ul> (<li>)
#ordered_list   ->      <ol> (<li>)