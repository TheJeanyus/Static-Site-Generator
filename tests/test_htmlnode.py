import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode()
        self.assertTrue(node.tag == None and node.value == None and node.children == None and node.props == None)

    def test_to_html(self):
        try:
            node = HTMLNode()
            node.to_html()  #Expected to throw implementation error
            self.assertTrue(False)
        except Exception as err:
            self.assertIsInstance(err, NotImplementedError)
    
    def test_props_string(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_print(self):
        child = HTMLNode()
        node = HTMLNode("a", "Learn to Code", [child], {"href":"boot.dev"})
        print_result = """<a href=\"boot.dev\">Learn to Code</a>
        Children: 1"""
        self.assertEqual(node.__repr__(), print_result)



if __name__ == "__main__":
    unittest.main()