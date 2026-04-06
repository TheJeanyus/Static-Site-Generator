import unittest
from src import converter

from src.textnode import TextNode, TextType
from src.markdownblock import MarkdownBlock, BlockType
from src.htmlnode import ParentNode


class TestConversions(unittest.TestCase):
    MD = """
## This is **bolded** heading

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

```
This is code
and this too
```

> That's what I said! - Me

1. This
2. Is
3. A
4. List



"""
    
    
    def test_split_bold(self):
        node = TextNode("This contains **BOLD Text** in the middle", TextType.TEXT)
        results = converter.split_nodes_delimiter([node], "**")
        #print(results)
        self.assertEqual(len(results), 3)
        self.assertTrue(results[1].text_type == TextType.BOLD)

    def test_split_italics(self):
        node = TextNode("This contains _Italic text_ in the middle", TextType.TEXT)
        results = converter.split_nodes_delimiter([node], "_")
        self.assertEqual(len(results), 3)
        self.assertTrue(results[1].text_type == TextType.ITALIC)

    def test_split_code(self):
        node = TextNode("This contains `Code text` in the middle", TextType.TEXT)
        results = converter.split_nodes_delimiter([node], "`")
        self.assertEqual(len(results), 3)
        self.assertTrue(results[1].text_type == TextType.CODE)

    def test_skip_typed_nodes(self):
        node = TextNode("This is **already** code", TextType.CODE)
        results = converter.split_nodes_delimiter([node], "**")
        self.assertEqual(node, results[0])
        
    def test_bad_delimiter(self):
        try:
            node = TextNode("This text doesn't matter", TextType.TEXT)
            results = converter.split_nodes_delimiter([node], "#")
        except Exception as e:
            self.assertEqual(str(e), "Unknown delimiter provided, cannot correctly type children")

    def test_no_end_delimiter(self):
        try:
            node = TextNode("Not **Actually Bold", TextType.TEXT)
            converter.split_nodes_delimiter([node], "**")
        except Exception as e:
            self.assertEqual(str(e), "An uneven number of delimters was found in: Not **Actually Bold")

    def test_multi_nodes(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT), 
                 TextNode("and this is not **italic** text", TextType.TEXT)]
        results = converter.split_nodes_delimiter(nodes, "**")
        self.assertEqual(len(results), 6)
        self.assertTrue(results[1].text_type == TextType.BOLD and results[4].text_type == TextType.BOLD)

    def test_eliminate_dead_nodes(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        results = converter.split_nodes_delimiter([node], "**")
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].text_type == TextType.BOLD)

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [LINK](https://i.imgur.com/3elNhQu.png) with an ending.",
            TextType.TEXT,
        )
        new_nodes = converter.split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("LINK", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with an ending.", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = converter.split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes
        )
    
    def test_extract_all_nodes(self):
        node = TextNode("This is **text** with an _italic_ word and a `code block` and an " \
        "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        new_nodes = converter.parse_text([node])
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            new_nodes
        )

    def test_markdown_to_blocks(self):
        blocks = converter.markdown_to_blocks(self.MD)
        self.assertEqual(
            blocks,
            [
                MarkdownBlock("## This is **bolded** heading", BlockType.HEADING),
                MarkdownBlock("This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", BlockType.PARAGRAPH),
                MarkdownBlock("- This is a list\n- with items", BlockType.UNORDERED_LIST),
                MarkdownBlock("```\nThis is code\nand this too\n```", BlockType.CODE),
                MarkdownBlock("> That's what I said! - Me", BlockType.QUOTE),
                MarkdownBlock("1. This\n2. Is\n3. A\n4. List", BlockType.ORDERED_LIST)
            ]
        )

    #TODO: Implement with full comparison
    def test_markdown_to_html_nodes(self):
        nodes = converter.markdown_to_html_nodes(self.MD)
        self.assertIsInstance(nodes, list)
        self.assertIsInstance(nodes[0], ParentNode)
        self.assertTrue(len(nodes) == 6)
        self.assertTrue(nodes[0].children is not None and len(nodes[0].children) == 3)

    def test_parse_paragraph(self):
        pass

    def test_parse_heading(self):
        pass

    def test_parse_codeblock(self):
        pass

    def test_parse_quote(self):
        pass

    def test_parse_list(self):
        pass

if __name__ == "__main__":
    unittest.main()