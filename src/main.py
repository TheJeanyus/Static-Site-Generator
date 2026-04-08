import os
import sys
import shutil
import re

from markdowndoc import MarkdownDoc
from htmltree import HTMLTree
from htmldoc import HTMLDoc

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    #base_dir = os.path.join(".", basepath)
    if not os.path.isdir(basepath):
        print("." + basepath)
        os.makedirs("." + basepath, exist_ok=True)
    copy_static(basepath)
    generate_content_recursive(basepath)
    
        



    pass

def generate_content_recursive(basepath:str, template_path:str = "./template.html"):
    content_dir = "./content"
    content_list = [os.path.join(content_dir, item) for item in os.listdir(content_dir)]
    while len(content_list) > 0:
        content = content_list.pop(0)
        if os.path.isfile(content):
            generate_content(basepath, content, template_path)
        else:
            content_list.extend([os.path.join(content, file) for file in os.listdir(content)])
    pass


def generate_content(basepath:str, src_path:str, template_path:str = "./template.html"):
    #content_dir = os.path.join(basepath, "content")
    #public_dir = os.path.join(basepath, "docs")
    dest_path = re.sub(r"content", r"docs", src_path)
    dest_path = re.sub(r".md$", r".html", dest_path)
    print(f"Generating {dest_path} from {src_path} from template {template_path}")
    markdown = MarkdownDoc.open_doc(src_path) 
    contents = HTMLTree.from_markdown_doc(markdown)
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok = True)
    html_doc = HTMLDoc(dest_path, contents)
    html_doc.write_doc(template_path, basepath)


def copy_static(basepath:str):
    public = "./docs"
    static = "./static"
    if os.path.exists(public):
        print(f"Clearing old data at {public}")
        shutil.rmtree(public)
    os.mkdir(public)
    file_list = os.listdir(static)
    while len(file_list) > 0:
        current = file_list.pop(0)
        src_path = os.path.join(static, current)
        dest_path = os.path.join(public, current)
        if os.path.isdir(src_path):
            os.mkdir(dest_path)
            print(f"Created dir at {dest_path}")
            file_list.extend([os.path.join(current, file) for file in os.listdir(src_path)])
        else:
            print(f"Copying {src_path} to {dest_path}...")
            shutil.copy(src_path, dest_path)
    return None

if __name__ == "__main__":
    main()

#heading        ->      <h1> to <h6>
#paragraph      ->      <p>
#code           ->      <pre><code>
#quote          ->      <blockquote>
#unordered_list ->      <ul> (<li>)
#ordered_list   ->      <ol> (<li>)