import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes :list[TextNode], delimiter :str, text_type :TextType):
    if delimiter not in ["**", "_", "`"]:
        raise Exception("Unknown delimiter provided, cannot correctly type children")
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        node_pieces = old_node.text.split(delimiter)
        if len(node_pieces) % 2 != 1:
            raise Exception(f"An uneven number of delimters was found in: {old_node.text}")
        new_nodes.extend(
            [TextNode(text, text_type if index % 2 else TextType.PLAIN) 
            for index, text in enumerate(node_pieces)]
            )
    new_nodes = [node for node in new_nodes if node.text != ""]
    return new_nodes

def extract_markdown_images(text:str):
    test = r"!\[(.+?)\]\((.+?)\)"
    return re.findall(test, text)
    
def extract_markdown_links(text:str):
    test = r"(?<!\!)\[(.+?)\]\((.+?)\)"
    return re.findall(test, text)
    