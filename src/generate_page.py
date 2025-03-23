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

def copy_static(source_path, dest_path):
        #New to a lot of these commands so will heavily annotate
        #source path will be "static", dest path will be "public"
        #use os.path.exists to check the public directory exists
        if os.path.exists(dest_path):
            #use shutil.rmtree to remove public (If it exists)
            shutil.rmtree(dest_path)
        #use os.mkdir to make public directory
        os.mkdir(dest_path)
        #list all items in the source
        source_files = os.listdir(source_path)
        #determine if its a directory or a file
        for file in source_files:
            source_file_path = os.path.join(source_path, file)
            dest_file_path = os.path.join(dest_path, file)
            if os.path.isfile(source_file_path):
                shutil.copy(source_file_path, dest_path)
                print(f"Copied file: {source_file_path} to {dest_path}")
            else:
                # Create the directory in the destination
                os.mkdir(dest_file_path)
                print(f"Created directory: {dest_file_path}")
                # Recursively copy the contents of this directory
                copy_static(source_file_path, dest_file_path)

def extract_title(markdown):
    split_block = markdown.split("\n")
    h1_lines = []
    for line in split_block:
          if re.match(r"^[#] ", line):
               h1_lines.append(line)
    if len(h1_lines) == 0:
        raise Exception("No <h1> line found. A valid <h1> line starts with exactly one #, followed by exactly one space, followed by the title")
    elif len(h1_lines) > 1:
        raise Exception("Multiple <h1> lines found")
    h1_line = h1_lines[0]
    cleaned_h1_line = h1_line.lstrip('#').strip()
    return cleaned_h1_line
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        from_path_contents = file.read()

    #print(f"Markdown content length: {len(from_path_contents)}")
    #print(f"First 100 chars: {from_path_contents[:100]}")

    with open(template_path, 'r') as file:
        template_path_contents = file.read() 
    html_node = markdown_to_html_node(from_path_contents)
    #print(f"HTML node type: {type(html_node)}")
    markdown_html = html_node.to_html()
    #print(f"Generated HTML length: {len(markdown_html)}")
    #print(f"First 100 chars of HTML: {markdown_html[:100]}")

    title = extract_title(from_path_contents)
    template_path_contents = template_path_contents.replace("{{ Title }}", title)
    template_path_contents = template_path_contents.replace("{{ Content }}", markdown_html)
    template_path_contents = template_path_contents.replace('href="/', f'href="{basepath}')
    template_path_contents = template_path_contents.replace('src="/', f'src="{basepath}')
    #print(f"Final HTML length: {len(template_path_contents)}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(template_path_contents)
        print(f"File should be written to {dest_path}")
        print(f"File exists: {os.path.exists(dest_path)}")
    
def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        relative_path = os.path.relpath(item_path, start='content')
        dest_path = os.path.join(dest_dir_path, relative_path)

        if os.path.isfile(item_path):
            dest_path = os.path.splitext(dest_path)[0] + '.html'
            generate_page(item_path, template_path, dest_path, basepath)
        else:
            generate_page_recursive(item_path, template_path, dest_dir_path, basepath)
        
            

