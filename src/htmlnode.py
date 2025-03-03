class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_string = ""
        for i in self.props:
            props_string += f' {i}="{self.props[i]}"'
        return props_string

    def __repr__(self):
        print(f" tag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props}")
