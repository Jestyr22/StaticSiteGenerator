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
        print("props:", self.props)
        return props_string

    def __repr__(self):
        print(f" tag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props}")

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, props=props, children=[])
        self.value = value

    def to_html(self):
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        


            


        




