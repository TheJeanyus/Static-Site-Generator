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

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        tree = HTMLTree.from_markdown_doc(md)
        html = tree.root.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        tree = HTMLTree.from_markdown_doc(md)
        html = tree.root.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()