from enum import Enum
import re
from htmlnode import HTMLNode
from extract_links import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from node_delimiter import find_delimiters, split_nodes_delimiter
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes
from node import text_node_to_html

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    split_block = markdown.split("\n\n") #splits the block based on double newlines
    stripped_block = [block.strip() for block in split_block] #strips leading/trailing spaces
    filtered_block = [block for block in stripped_block if block] #filters out empty lines from the list
    return filtered_block

def block_to_block_type(markdown): #Takes a single item from the list markdown_to_blocks returns

    #Headings start with 1-6 # characters, followed by a space and then the heading text.
    if re.match(r"^[#]{1,6} ", markdown):
        # ^ means starts with, [#] means searching for #, {1,6} means searching for 1-6, and the trailing space is intentional
        return BlockType.HEADING
    
    #Code blocks must start with 3 backticks and end with 3 backticks.
    if re.match(r"^```[\s\S]*```$", markdown):
        # ```$ means "ends with ```", [\s\S] means it matches all content, regardless of characters or newlines
        return BlockType.CODE
    
    #Every line in a quote block must start with a > character.
    if re.match(r"^(>.*\n?)*$", markdown):
        #>.* matches a single line that starts with >, followed by any amount of text. \n? accounts for optional newlines, to handle multiple lines of quotes
        return BlockType.QUOTE
    
    #Every line in an unordered list block must start with a - character, followed by a space.
    if re.match(r"^(- .*\n?)*$", markdown):
        #Same regex as quote, just switched ">" for "- "
        return BlockType.UNORDERED_LIST
    
    #Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    if re.match(r"^\d+\. ", markdown):
        #\d means starts with any digit, '+\. ' means immediately followed by a period and a space
        markdown_list = markdown.split("\n")
        counter = 1
        for line in markdown_list:
            number = int(line.split(".")[0]) #Extracts the number before .
            if number != counter: #If the first number doesn't match the counter, it isn't ordered
                return BlockType.PARAGRAPH
            counter += 1
        return BlockType.ORDERED_LIST
    
    #If none of the above conditions are met, the block is a normal paragraph.
    return BlockType.PARAGRAPH

    '''Very proud of this one. I have a habit of going overboard with annotations (Self-fulfilling prophecy right here),
    but this has nice, simple annotations to explain the criteria each part is looking for, and an explaination of the
    regex filter because I will doubtless forget what each part means. It's not exactly complicated, but I'm incredibly
    happy with my work here.'''

'''
Paragraph blocks → <p> tags
Heading blocks → <h1> to <h6> tags (depending on heading level)
Code blocks → <pre><code> tags
Unordered list blocks → <ul> with <li> for each item
Ordered list blocks → <ol> with <li> for each item
Quote blocks → <blockquote> tags

Block to HTML lesson notes:
Function markdown_to_html_node will recieve a string of text
Break that string down using existing function markdown_to_blocks
For each block:
- Determine its BlockType using block_to_block_type
- Convert it to appropriate HTMLNode (Create a new function for this?)
- Run each HTMLNode through previously made text_to_text_nodes function (In text_to_textnodes.py)
(This will handle bold, italic, links, images)
(DO NOT RUN CODE BLOCKS THROUGH THIS)
Combine all block level HTMLNodes as children under one parent div HTMLNode
'''
def count_heading_level(block):
    #helper function to count the number of leading #s, returns an integer
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    return level

def code_to_text_node(block):
    #helper function to strip leading/trailing backticks from code blocks, returns a TextType.TEXT Textnode
    lines = block.split("\n")
    # Remove the first and last line if they contain backticks
    if lines and lines[0].strip().startswith("```"):
        lines.pop(0)
    if lines and lines[-1].strip().startswith("```"):
        lines.pop(-1)
    text = "\n".join(lines)
    code_textnode = TextNode(text, TextType.TEXT)
    return code_textnode

def text_node_list_to_html(text_nodes):
    #helper function to run lists through text_node_to_html
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html(text_node)
        html_nodes.append(html_node)
    return html_nodes

def unordered_ordered_list_to_html_nodes(block):
    #helper function to split UNORDERED/ORDERED_LIST blocks into actual Python lists, then run that list through text_to_text_node
    lines = block.strip().split("\n")
    list_items = []
    for line in lines:
        # For unordered lists
        if line.startswith("- "):
            content = line[2:]  # Skip the "- " prefix
        
        else:
        # For ordered lists
            match = re.match(r"\d+\.\s+", line)  # Find the position after the first period and space, skipping the "1. " etc
            if match:
                content = line[match.end():]
        text_nodes = text_to_textnodes(content)
        html_nodes = text_node_list_to_html(text_nodes)
        list_items.append(HTMLNode("li", None, html_nodes))
    return list_items

def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        text_nodes = text_to_textnodes(block)
        html_nodes = text_node_list_to_html(text_nodes)
        return HTMLNode("p", None, html_nodes)
    elif block_type == BlockType.HEADING:
        heading_level = count_heading_level(block)
        heading_text = block.lstrip("#").strip()
        text_nodes = text_to_textnodes(block)
        html_nodes = text_node_list_to_html(text_nodes)
        return HTMLNode(f"h{heading_level}", None, html_nodes)
    elif block_type == BlockType.CODE:
        code_block = code_to_text_node(block)
        code_node = HTMLNode("code", None, text_node_to_html(code_block))
        return HTMLNode("pre", None, code_node)
    elif block_type == BlockType.QUOTES:
        text_nodes = text_to_textnodes(block)
        html_nodes = text_node_list_to_html(text_nodes)
        return HTMLNode("blockquote", None, html_nodes)
    elif block_type == BlockType.UNORDERED_LIST:
        html_nodes = unordered_ordered_list_to_html_nodes(block)
        return HTMLNode("ul", None, html_nodes)
    elif block_type == BlockType.ORDERED_LIST:
        html_nodes = unordered_ordered_list_to_html_nodes(block)
        return HTMLNode("ol", None, html_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = HTMLNode("div", None, [])
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        parent_node.children.append(block_node)
    return parent_node
