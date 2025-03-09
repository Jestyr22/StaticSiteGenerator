from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html(text_node):
    mapping = { #Dictionary used to reduce amount of if statements needed. If it's in the dictionary, it follows the same basic structure (<tag> text </tag>)
     TextType.BOLD: "b",
     TextType.ITALIC: "i",
     TextType.CODE: "code",
    }
    tag = mapping.get(text_node.type)

    if text_node.type == TextType.TEXT: #Should be above the "mapping" dictionary for order of operations, but grouping with the rest of the if statements for readability
        return LeafNode(text_node.text) 

    elif tag: #If the TextType appears in the mapping dictionary
        return LeafNode(text_node.text, tag=tag)
    
    elif text_node.type == TextType.LINK:
        return LeafNode(text_node.text, tag ="a", props={"href": text_node.href})
        
    elif text_node.type == TextType.IMAGE:
        return LeafNode("", tag="img", props={"src": text_node.src, "alt": text_node.alt})
    
    else:
        raise Exception #Catch-All in case the tag isn't in this list