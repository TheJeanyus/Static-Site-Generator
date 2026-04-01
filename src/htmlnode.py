

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        #Children will override
        raise NotImplementedError
    
    def props_to_html(self):
        prop_string = ""
        if self.props != None and self.props != {}:
            for prop in self.props:
                prop_string += f" {prop}=\"{self.props[prop]}\""
        return prop_string
    
    def __repr__(self):
        return f"""<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>
        Children: {len(self.children) if self.children != None else None}"""


