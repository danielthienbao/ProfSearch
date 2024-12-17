import pdfplumber
import re

def extract_text_with_pdfplumber(pdf_path):
    """Extract text from a PDF."""
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text

def search_by_professor(full_text, name_query):
    """Search for professor's data."""
    matching_lines = []
    lines = full_text.split("\n")
    for line in lines:
        if all(part.lower() in line.lower() for part in name_query.split()):
            matching_lines.append(line)
    
    if not matching_lines:
        return f"No data found for '{name_query}'."
    
    return matching_lines

def search_by_class(full_text, class_name):
    """Search for class-related data."""
    cleaned_text = re.sub(r"\s+", " ", full_text)
    pattern = rf"({class_name})\s+([\w\s,]+?)\s+(ECC|ONLIN|HYBRD)\s+(\d+%)\s+(\d+%)"
    matches = re.findall(pattern, cleaned_text)

    if not matches:
        return f"No data found for class '{class_name}'."
    
    table_data = [[prof.strip(), course, method, success, completion] 
                  for course, prof, method, success, completion in matches]
    return sorted(table_data, key=lambda x: (-int(x[3].replace('%', '')), -int(x[4].replace('%', ''))))
    