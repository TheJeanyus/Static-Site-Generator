class MarkdownDoc:
    def __init__(self, contents:str):
        self.contents = contents

    def __repr__(self):
        return self.contents
    
    #Opening and file capabilities
    @classmethod
    def open_doc(cls, path):
        with open(path, "r") as f:
            text = f.read()
            f.close()
        return MarkdownDoc(text)
            