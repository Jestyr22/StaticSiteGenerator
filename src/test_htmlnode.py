import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_basic(self):
        
        node = HTMLNode(props={"href": "https://url.com", "target": "URL"})
        expected = ' href="https://url.com" target="URL"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")