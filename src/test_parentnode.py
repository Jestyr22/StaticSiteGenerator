import unittest

from htmlnode import LeafNode, ParentNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_children(self):
        child1 = LeafNode(tag="span", value="Child1")
        child2 = LeafNode(tag="span", value="Child2")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><span>Child1</span><span>Child2</span></div>")

    def test_with_props(self):
        child = LeafNode(tag="span", value="text")
        parent = ParentNode(tag="div", children=[child], props={"class": "container", "id": "main"})

    def test_missing_tag(self):
        node = ParentNode(tag=None, children=[LeafNode("span", "text")])
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_missing_children(self):
        node = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            node.to_html()