import unittest

from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType
from node import text_node_to_html

'''
Test List
Basic node
Bold node
Italic node
Code node
Link node
Image node
Missing tag node
Invalid tag node
Link node no href
Image node no src
Image node no alt
'''

class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode(text="This is a text node", text_type=TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode(text="This is a bold text node", text_type=TextType.BOLD)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode(text="This is an italic text node", text_type=TextType.ITALIC)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode(text="This is a code node", text_type=TextType.CODE)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode(text="This is a link", text_type=TextType.LINK, url="www.URL.com")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "www.URL.com")

    def test_image(self):
        node = TextNode(text="This is an image", text_type=TextType.IMAGE, url="www.URL.com/image.png")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIn("src", html_node.props)
        self.assertEqual(html_node.props["src"], "www.URL.com/image.png")
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["alt"], "This is an image")

    def test_invalid_text_type(self):
        invalid_node = TextNode("Some text", "NOT_A_VALID_TYPE")
        with self.assertRaises(Exception):
            text_node_to_html(invalid_node)

    def test_missing_text_type(self):
        invalid_node = TextNode("Some text", None)
        with self.assertRaises(Exception):
            text_node_to_html(invalid_node)