import re

from textnode import TextType, TextNode
from markdowndoc import MarkdownDoc
from markdownblock import BlockType, MarkdownBlock


#Helper for conversion that are one-to-many or many-to-many
class converter:
    BLOCK_PATTTERN = re.compile(r"(?P<heading>#+\x20.*)|"\
                        r"(?P<code>```\n[^`]*\n```)|"\
                        r"(?P<quote>(?:^>\x20?.*\n)*)|"\
                        r"(?P<unordered_list>(?:^-\x20.*\n)*)|"\
                        r"(?P<ordered_list>(?:^\d\.\x20.*\n)*)|"\
                        r"(?P<paragraph>^\n([^#`>\-\d](?:.+\n)*))", 
                        flags=re.MULTILINE)
    
    IMAGE_PATTERN = re.compile(r"!\[(.*?)\]\((.+?)\)")

    LINK_PATTERN = re.compile(r"(?<!\!)\[(.+?)\]\((.+?)\)")

    DELIMITER_MAP = {
                    "**":TextType.BOLD,
                    "_":TextType.ITALIC,
                    "`":TextType.CODE
                    }

    def markdown_to_blocks(self, doc:MarkdownDoc):
        m = re.finditer(self.BLOCK_PATTTERN, doc.contents)
        full_list = [x.groupdict() for x in m if x.group() != ""]
        block_list:list[MarkdownBlock] = []
        for block_dict in full_list:
            for key in block_dict:
                if block_dict[key] is not None and block_dict[key].strip() != "":
                    block_list.append(MarkdownBlock(block_dict[key].strip(), BlockType(key)))
        #print(block_list)
        return block_list

    def split_nodes_delimiter(self, old_nodes:list[TextNode], delimiter:str):
        if delimiter not in self.DELIMITER_MAP:
            raise Exception("Unknown delimiter provided, cannot correctly type children")
        text_type = self.DELIMITER_MAP[delimiter]
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

    def extract_markdown_images(self, text:str):
        return re.findall(self.IMAGE_PATTERN, text)
        
    def extract_markdown_links(self, text:str):
        return re.findall(self.LINK_PATTERN, text)

    def split_nodes_images(self, old_nodes:list[TextNode]):
        new_nodes:list[TextNode] = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            images = self.extract_markdown_images(old_node.text)
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

    def split_nodes_links(self, old_nodes:list[TextNode]):
        new_nodes:list[TextNode] = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            links = self.extract_markdown_links(old_node.text)
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

    def parse_text(self, old_nodes):
        return self.split_nodes_delimiter(
            self.split_nodes_delimiter(
                self.split_nodes_delimiter(
                    self.split_nodes_images(
                        self.split_nodes_links(
                            old_nodes
                        )
                    )
                , "_")
            , "`"), 
        "**")        
