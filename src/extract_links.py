import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = [] #Empty list to store new nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node) #Checks that the nodes aren't TEXT, if they are they're added to the list as is
            continue

        extracted_images = extract_markdown_images(node.text)
        if not extracted_images:
            new_nodes.append(node) #If extract_markdown_images comes back empty, there's no image to add, so add node as is
            continue

        remaining_text = node.text
        for image_text, url in extracted_images:
            markdown_image = f"![{image_text}]({url})" #Combines the tuples returned by extract function, and loops through each set of tuples
            parts = remaining_text.split(markdown_image, 1) #Splits the node based on the returned tuple

            if parts[0]: #Checks for parts *before* the image to add as .TEXT
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(image_text, TextType.IMAGE, url)) #Otherwise, add the isolated markdown syntax to the list as .IMAGE

            if len(parts) > 1: #If there's more than one part, set remaining_text to anything not gone through yet, and start the loop again
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT)) #add any text that's leftover as .TEXT, as it'll contain no images
    return new_nodes        



def split_nodes_link(old_nodes): #Will not annotate as this is basically identical to images, just adjusted to work for links instead
    new_nodes = [] 
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node) 
            continue

        extracted_links = extract_markdown_links(node.text)
        if not extracted_links:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for link_text, url in extracted_links:
            markdown_link = f"[{link_text}]({url})"
            parts = remaining_text.split(markdown_link, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes  