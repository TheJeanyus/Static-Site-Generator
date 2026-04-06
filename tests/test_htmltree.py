import unittest

from src.htmltree import HTMLTree
from src.htmlnode import LeafNode


class TestHTMLTree(unittest.TestCase):
    def test_init(self):
        node = LeafNode("p", "A tree")
        tree = HTMLTree(node)
        self.assertIsInstance(tree, HTMLTree)

    def test_from_markdown(self):
        doc = """
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
        tree = HTMLTree.from_markdown_doc(doc)
        self.assertIsInstance(tree, HTMLTree)
        self.assertTrue(tree.root.tag == "div")
        self.assertTrue(tree.root.children is not None and len(tree.root.children) == 6)

if __name__ == "__main__":
    unittest.main()