from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #Goal is to split a text node value into 3 nodes. The text_type, and the parts before and after
    #So "This is text with a 'code block' word" becomes:
    #"This is text with a"
    #"code block"
    #"word"
    #Delimiter is the symbols surrounding what would be code ('), bold (**) or italic (_)
    
    '''Find the first instance of the opening delimiter
Find the matching closing delimiter
Create a text node for the content before the first delimiter (as TEXT type)
Create a text node for the content between delimiters (with the special type)
Repeat for any remaining text'''

    new_nodes = [] #Empty list to add completed nodes to

    for old_node in old_nodes: #Loops through the list

        if old_node.text_type != TextType.TEXT: #Checks for non-TEXT nodes
            new_nodes.append(old_node) #Adds non-TEXT nodes to new_nodes as they need no further delimiting
        text = old_node.text #To save me having to write old_node.text every time I refer to this
        sections = find_delimiters(text, delimiter) #Sends all text through to find delimiter pairs, returns a list of all text, split by delimiter
        
        for section in sections: #Loops through the list
            text_content, is_delimited = section
            if text_content:  # Only add if there's content
                node_type = text_type if is_delimited else TextType.TEXT #Checks if content needs a special tag using the True/False in find_delimiters, and assigns it the tag if needed
                new_nodes.append(TextNode(text_content, node_type)) #Adds the new text to the new_nodes list, with the correct tag

    return new_nodes
                                    


        
def find_delimiters(text, delimiter): #New function to find pairs of delimiters
    current_position = 0 #Counter to find the delimiters in old_node.text
    result = [] #Empty list to store all results
    
    if delimiter not in text: #Checks for delimiter existence
        result.append((text, False)) #Adds text to result list
        return result #Returns early because if there's no delimiter, it's already as split as can be
    while current_position < len(text): #Loops through until it's gone through all characters in text
        
        opening_position = text.find(delimiter, current_position) #Finds first delimiter
        if opening_position == -1: #If no more delimiters are found
            break #exits loop

        closing_position = text.find(delimiter, opening_position + len(delimiter)) #Finds first delimiter **after** the one at opening_position (Hence adding the length of the delimiter)
        if closing_position == -1: #If there's not a closing delimiter
            raise ValueError(f"No closing delimiter '{delimiter}'") #Raise an error because they should always come in pairs
        
        content = text[opening_position + len(delimiter):closing_position]  #Extracts the content between delimiters.
                                                                            #opening_position + len() to find the first character after first delimiter,
                                                                            #closing_position to find the endpoint
        
        pre_content = text[current_position:opening_position] #Gets the text before first delimiter
        result.append((pre_content, False)) #Adds to list, False indicates that it doesn't need a special tag, and is just text
        result.append((content, True))
        current_position = closing_position + len(delimiter) #Sets current position to after the pair has been found
    if current_position < len(text):
        result.append((text[current_position:], False)) #Adds text after final delimiter to result
    return result


        




