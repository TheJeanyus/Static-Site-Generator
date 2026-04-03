import re

from parseblockmarkdown import BlockType, MarkdownBlock, markdown_to_blocks
from parseinlinemarkdown import parse_text
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

def main():
    
    pass

def markdown_to_html_node(markdown:str):
    block_list = markdown_to_blocks(markdown)
    div_children = []
    for block in block_list:
        text_nodes = parse_text(block.text)
        block_children = [text_node.text_node_to_html_node for text_node in text_nodes]
        block_node_tag = ""
        block_node = ParentNode(block_node_tag, block_children)
        div_children.append(block_node)
    div_node = ParentNode("div", div_children)
    return div_node

if __name__ == "__main__":
    main()

#heading        ->      <h1> to <h6>
#paragraph      ->      <p>
#code           ->      <pre><code>
#quote          ->      <blockquote>
#unordered_list ->      <ul> (<li>)
#ordered_list   ->      <ol> (<li>)