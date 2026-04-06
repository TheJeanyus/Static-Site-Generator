import unittest

from src.markdowndoc import MarkdownDoc
from src.markdownblock import BlockType, MarkdownBlock


class TestMarkdownClasses(unittest.TestCase):
    def test_init_doc(self):
        doc = MarkdownDoc("# This is a markdown doc")
        self.assertIsInstance(doc, MarkdownDoc)

    def test_init_block(self):
        block = MarkdownBlock("This is a paragraph", BlockType.PARAGRAPH)
        self.assertIsInstance(block, MarkdownBlock)
        self.assertTrue(block.block_type == BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()