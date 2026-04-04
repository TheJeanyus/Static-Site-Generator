class MarkdownDoc:
    def __init__(self, contents:str):
        self.contents = contents

    def __repr__(self):
        return self.contents
    
    #Opening and file capabilities