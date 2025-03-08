class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_string = ""
        for i in self.props:
            props_string += f' {i}="{self.props[i]}"'
        #print("props:", self.props) #added for debugging purposes
        return props_string

    def __repr__(self):
        print(f" tag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props}")

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        #Note: I messed up here by having the variables in a different order to HTMLNode. Not an issue for this scenario,
        #but could be an issue in real-life situations. Will use LeafNode order going forward though
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag=tag, props=props, children=[])
        self.value = value

    def to_html(self):
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        #return "props_to_html" of node *and* children recursively
        children_to_html = ""
        for child in self.children:
            children_to_html += str(child.to_html())
        return (f"<{self.tag}>{children_to_html}</{self.tag}>")
    


        


            


        




