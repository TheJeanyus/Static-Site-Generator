import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_init(self):
        try:
            node1 = TextNode("This is plain text", TextType.TEXT)
            node2 = TextNode("This is bold text", TextType.BOLD)
            node3 = TextNode("This is italic text", TextType.ITALIC)
            node4 = TextNode("This is code", TextType.CODE)
            node5 = TextNode("This is a link", TextType.LINK, url="http://localhost:8888")
            node6 = TextNode("This is an image", TextType.IMAGE, url="http://localhost:8888")
        except Exception as e:
            self.assertIsInstance(None, TextNode)

    
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, url="www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_type(self):
        node1 = TextNode("This is the same text", TextType.BOLD, url="www.google.com")
        node2 = TextNode("This is the same text", TextType.ITALIC, url="www.google.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is a link node", TextType.LINK, "boot.dev")
        self.assertEqual(node.__repr__(), "TextNode(This is a link node, link, boot.dev)")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "boot.dev")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"boot.dev"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "imgur.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"imgur.com", "alt":"This is an image node"})

if __name__ == "__main__":
    unittest.main()