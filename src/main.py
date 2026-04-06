import sys
import os
import shutil

def main():
    copy_static()
    
        
        



    pass

def copy_static():
    public = "./public"
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