import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_valid_tag(self):
        node = LeafNode("content", "div")
        self.assertEqual(node.to_html(), "<div>content</div>")

    def test_leaf_no_value(self): 
        with self.assertRaises(ValueError):
            node = LeafNode(None, "p")
            node.to_html()
            '''Learnt a valuable lesson not to just copy/paste tests from Boot.Dev
            The example tests passed Value and Tag in the wrong order, so test 1 didn't work because it was outputting <content>div</content>
            and test 2 didn't work because it was passing "p" as a value, so didn't need to raise the error
            Switched em around, and now it works fine!'''

    def test_leaf_no_tag(self):
        node = LeafNode("Just text, no tag")
        self.assertEqual(node.to_html(), "Just text, no tag")

    def test_leaf_with_attributes(self):
        node = LeafNode( "Click me!", "a",props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev" target="_blank">Click me!</a>')
#   This test doesn't work, gotta troubleshoot
#   A note to future me: Not specifying "props" from the test as "props" in the LeafNode caused all sorts of issues.
#   the intended "props" was being assigned incorrectly, so not being passed to props_to_html, so when that came back without props,
#   it was working perfectly, just being handed the wrong information.
#   Two days of troubleshooting, because I forgot about the order it was all assigned in.
#   I am a fool.

