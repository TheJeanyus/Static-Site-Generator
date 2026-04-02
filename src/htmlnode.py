

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


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return self.to_html()

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value = None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        if self.children is None or self.children == []:
            raise ValueError("Parent node must contain at least one child node")
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string