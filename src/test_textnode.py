import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_init(self):
        try:
            node1 = TextNode("This is plain text", TextType.PLAIN)
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


if __name__ == "__main__":
    unittest.main()