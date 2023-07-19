"""Converts a html/based docs folder to markdowns files
"""

import markdownify
import os
import re
import pickle


def find_line_number(string, text):
    for i, line in enumerate(text, start=1):
        if string in line:
            return i
    return -1  # String not found

def replace_extension(match):
    if "http" in match.group(0):
        return match.group(0)
    else:
        return match.group(1) + ".md"
    
def replace_images(match):
    print(f"[{match.group(1)}](/{match.group(2)})")
    return f"[{match.group(1)}](/{match.group(2)})"

def replace_with_dict(match):
    with open('person_data.pkl', 'rb') as fp:
        dictionary_precompilato = pickle.load(fp)

    value = dictionary_precompilato[match.group(1)]
    return f"[{match.group(1)}](<{value}>)"

def create_subfolders_from_lines(text, complete_dict):
    lines = text.splitlines()
    start_index = find_line_number("AU Static", lines)
    page_title = lines[start_index-1][26:]
    title_path = page_title.replace(" ", "-")
    current_folder = r"C:\Users\HW5584\Git\au_static_test_software\docs\AUSTS\markdowns"
    subfolder_hierarchy = []  # Keep track of the subfolder hierarchy
    hierarchy = 0

    for line in lines[start_index:]:
        match = re.match(r"\d+\.\s+\[(.*?)\]", line)
        if match:
            folder_name = match.group(1)
            subfolder_hierarchy.append(folder_name.replace(" ", "-"))
            hierarchy += 1
        elif line == "":
            continue
        else:
            break

    if subfolder_hierarchy:
        subfolder_path = os.path.join(current_folder, *subfolder_hierarchy)
        relative_subfolder = os.path.join(*subfolder_hierarchy)
        os.makedirs(subfolder_path, exist_ok=True)
        hierarchy_path = r"..\\"*hierarchy
        if page_title in complete_dict:
            complete_dict[page_title] = f"/{relative_subfolder}\{title_path}.md"
            if page_title == "AU Static Test Software":
                complete_dict[page_title] = r"/index.md"
    else: 
        subfolder_path = current_folder

    return rf"{subfolder_path}\{title_path}.md", complete_dict  # Return the current folder if no subfolders are created


if __name__ == "__main__":
    # Get all HTML files in the folder
    html_files = [f for f in os.listdir("docs\AUSTS\html") if f.endswith('.html')]
    folder_path = r"C:\Users\HW5584\Git\au_static_test_software\docs\AUSTS\html"
    folder_path_mkdows = r"C:\Users\HW5584\Git\au_static_test_software\docs\AUSTS\markdowns"
    # os.mkdir(fr"{folder_path}\markdowns")
    complete_dict = {}


    for file_path in html_files:
        with open(fr"{folder_path}\{file_path}", 'r', encoding="utf8") as file:
            html_content = file.read()
            new_content = re.sub(r'(\b(https?)?([-:/\.A-Za-z0-9_]+\b))\.html\b', replace_extension, html_content, count=0)
            markdown_text = markdownify.markdownify(new_content)
            matches = re.findall(r'\[([^\]]+)\]\((.+\.md)\)', markdown_text)
            for match in matches:
                complete_dict[match[0]] = match[1]

            _, _ = create_subfolders_from_lines(markdown_text, complete_dict)

    for file_path in html_files:
        with open(fr"{folder_path}\{file_path}", 'r', encoding="utf8") as file:
            html_content = file.read()
            new_content = re.sub(r'(\b(https?)?([-:/\.A-Za-z0-9_]+\b))\.html\b', replace_extension, html_content, count=0)
            markdown_text = markdownify.markdownify(new_content)


            _, complete_dict = create_subfolders_from_lines(markdown_text, complete_dict)

    with open('person_data.pkl', 'wb') as fp:
        complete_dict["AU Static Test Software"] = r"/index.md"
        pickle.dump(complete_dict, fp)
        print('dictionary saved successfully to file')

    for file_path in html_files:
        with open(fr"{folder_path}\{file_path}", 'r', encoding="utf8") as file:
            html_content = file.read()
            new_content = re.sub(r'(\b(https?)?([-:/\.A-Za-z0-9_]+\b))\.html\b', replace_extension, html_content, count=0)
            markdown_text = markdownify.markdownify(new_content)
            new_content = re.sub(r'\[([^\]]+)\]\((.+\.md)\)', replace_with_dict, markdown_text, count=0)
            new_content = re.sub(r'\[(.*)\]\((.+(?:\.png)|(?:\.jpeg)|(?:\.jpg))\)', replace_images, new_content, count=0)
            subfolder_path, _ = create_subfolders_from_lines(markdown_text, complete_dict)

        with open(rf"{subfolder_path}", 'w', encoding="utf8") as markdown_file:
            markdown_file.write(new_content)
