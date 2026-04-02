import re
from textnode import TextType, TextNode

delimiter_map = {
"**":TextType.BOLD,
"_":TextType.ITALIC,
"`":TextType.CODE
}

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str):
    if delimiter not in delimiter_map:
        raise Exception("Unknown delimiter provided, cannot correctly type children")
    text_type = delimiter_map[delimiter]
    new_nodes = []
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

def extract_markdown_images(text:str):
    test = r"!\[(.*?)\]\((.+?)\)"
    return re.findall(test, text)
    
def extract_markdown_links(text:str):
    test = r"(?<!\!)\[(.+?)\]\((.+?)\)"
    return re.findall(test, text)

def split_nodes_images(old_nodes:list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        temp = old_node.text
        for image in images:
            text, temp = temp.split(f"![{image[0]}]({image[1]})", 1)
            new_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        new_nodes.append(TextNode(temp, TextType.TEXT))
    new_nodes = [node for node in new_nodes if (node.text != "" or node.text_type == TextType.IMAGE)]
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        temp = old_node.text
        for link in links:
            text, temp = temp.split(f"[{link[0]}]({link[1]})", 1)
            new_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
        new_nodes.append(TextNode(temp, TextType.TEXT))
    new_nodes = [node for node in new_nodes if node.text != ""]
    return new_nodes

#def parse_text(old_nodes):
#    return split_nodes_delimiter()