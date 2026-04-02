import unittest

from parsemarkdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestConversions(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This contains **BOLD Text** in the middle", TextType.PLAIN)
        results = split_nodes_delimiter([node], "**", TextType.BOLD)
        #print(results)
        self.assertEqual(len(results), 3)
        self.assertTrue(results[1].text_type == TextType.BOLD)

    def test_split_italics(self):
        node = TextNode("This contains _Italic text_ in the middle", TextType.PLAIN)
        results = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(results), 3)
        self.assertTrue(results[1].text_type == TextType.ITALIC)

    def test_split_code(self):
        node = TextNode("This contains `Code text` in the middle", TextType.PLAIN)
        results = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(results), 3)
        self.assertTrue(results[1].text_type == TextType.CODE)

    def test_skip_typed_nodes(self):
        node = TextNode("This is **already** code", TextType.CODE)
        results = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node, results[0])
        
    def test_bad_delimiter(self):
        try:
            node = TextNode("This text doesn't matter", TextType.PLAIN)
            results = split_nodes_delimiter([node], "#", TextType.BOLD)
        except Exception as e:
            self.assertEqual(str(e), "Unknown delimiter provided, cannot correctly type children")

    def test_no_end_delimiter(self):
        try:
            node = TextNode("Not **Actually Bold", TextType.PLAIN)
            split_nodes_delimiter([node], "**", TextType.BOLD)
        except Exception as e:
            self.assertEqual(str(e), "An uneven number of delimters was found in: Not **Actually Bold")

    def test_multi_nodes(self):
        nodes = [TextNode("This is **bold** text", TextType.PLAIN), 
                 TextNode("and this is not **italic** text", TextType.PLAIN)]
        results = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(results), 6)
        self.assertTrue(results[1].text_type == TextType.BOLD and results[4].text_type == TextType.BOLD)

    def test_eliminate_dead_nodes(self):
        node = TextNode("**Bold** at the start", TextType.PLAIN)
        results = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].text_type == TextType.BOLD)

if __name__ == "__main__":
    unittest.main()