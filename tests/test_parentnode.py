import unittest

from src.htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node1 = LeafNode(None, "This is a ")
        grandchild_node2 = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node], {"class":"warning"})
        self.assertEqual(
            parent_node.to_html(),
            "<div class=\"warning\"><span>This is a <b>grandchild</b></span></div>",
        )



if __name__ == "__main__":
    unittest.main()