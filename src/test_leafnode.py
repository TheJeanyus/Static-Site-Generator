import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click Here", {"href":"boot.dev"})
        self.assertEqual(node.to_html(), "<a href=\"boot.dev\">Click Here</a>")

    def test_leaf_to_html_val(self):
        node = LeafNode(None, "Click Here")
        self.assertEqual(node.to_html(), "Click Here")
