import os
import shutil
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from extract_links import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from node_delimiter import find_delimiters, split_nodes_delimiter
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes
from node import text_node_to_html
from blocks import *
from generate_page import copy_static, generate_page, extract_title, generate_page_recursive
import sys
def main ():
    #docs_path = os.path.join(os.getcwd(), "docs")
    #print(f"Docs directory: {docs_path}")
    #print(f"Docs exists: {os.path.exists(docs_path)}")

    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
    copy_static("static", "docs")
    generate_page_recursive("content", "template.html", "docs", basepath)
    

    
    '''
    test_md = "# Test Heading\n\nThis is a paragraph."
    test_node = markdown_to_html_node(test_md)
    print(test_node.to_html())
    '''

if __name__ == "__main__":
    main()