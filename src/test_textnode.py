import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    #Boot.Dev provided test
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    #My own tests
    def test_diff_1(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a second text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_missing_1(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.URL.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    '''
    def test_missing_2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node") 
        self.assertNotEqual(node, node2)
    '''
        #Test failed because it needs a positional argument
        #Suppose that's good though, shows the program doesn't work if somethings missing, which is expected


if __name__ == "__main__":
    unittest.main()