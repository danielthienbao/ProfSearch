# to run: python professor_stats.py
import os
import pdfplumber
from tabulate import tabulate
import re  # Add regex for precise matching

# Function to extract text from the PDF using pdfplumber
def extract_text_with_pdfplumber(pdf_path):
    full_text = ""
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found. Please check the file path.")
        return None
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    if not full_text.strip():
        print("Error: Could not extract text from the PDF. Please ensure it is not an image-based PDF.")
        return None
    return full_text

# Function to search for professors by name
def search_by_professor(full_text):
    name_query = input("\nEnter the professor's first name, last name, or both: ").strip()
    matching_lines = []
    lines = full_text.split("\n")
    for line in lines:
        if all(part.lower() in line.lower() for part in name_query.split()):
            matching_lines.append(line)

    if not matching_lines:
        print(f"No data found for '{name_query}'. Please check the name and try again.")
        return

    if len(matching_lines) > 1:
        print(f"\nMultiple matches found for '{name_query}'. Please choose one:")
        table_data = []
        for i, line in enumerate(matching_lines, start=1):
            table_data.append([i, line])
        print(tabulate(table_data, headers=["Option", "Professor Details"], tablefmt="grid"))

        try:
            choice = int(input("\nEnter the number corresponding to the professor: ").strip()) - 1
            if 0 <= choice < len(matching_lines):
                display_professor_details(matching_lines[choice])
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the professor.")
    else:
        display_professor_details(matching_lines[0])

def search_by_class(full_text):
    # Ask for class input
    class_name = input("\nEnter the class name or code (e.g., MATH-270): ").strip().upper()
    
    # Clean the text to merge lines for more robust matching
    cleaned_text = re.sub(r"\s+", " ", full_text)  # Replace all whitespace with a single space
    
    # Regex pattern to find course followed by professor details
    pattern = rf"({class_name})\s+([\w\s,]+?)\s+(ECC|ONLIN|HYBRD)\s+(\d+%)\s+(\d+%)"
    matches = re.findall(pattern, cleaned_text)

    # Handle no matches
    if not matches:
        print(f"No data found for class '{class_name}'. Please check the name and try again.")
        return

    # Prepare and display the table
    table_data = []
    for match in matches:
        course, professor, method, success_rate, completion_rate = match
        table_data.append([professor.strip(), course, method, success_rate, completion_rate])

    # Sort by success rate and completion rate
    sorted_data = sorted(table_data, key=lambda x: (-int(x[3].replace('%', '')), -int(x[4].replace('%', ''))))

    print("\nProfessors for class sorted by Success and Completion Rates:\n")
    print(tabulate(sorted_data, headers=["Professor", "Course", "Method", "Success Rate", "Completion Rate"], tablefmt="grid"))

# Function to display detailed professor statistics
def display_professor_details(professor_line):
    fields = professor_line.split()
    table_headers = [
        "Division", "Course", "Professor", "Method", "Success Rate (%)",
        "Completion Rate (%)", "A", "B", "C", "IPP", "D", "F", "INP", "W", "Total"
    ]

    if len(fields) < len(table_headers):
        fields.extend(["-"] * (len(table_headers) - len(fields)))

    data = [fields[:len(table_headers)]]
    print("\nStatistics for the selected professor:\n")
    print(tabulate(data, headers=table_headers, tablefmt="grid"))

# Main function to handle user input
def main():
    pdf_path = "SuccCompletion_Sp24_Instruct.pdf"  # Update with the correct path to your PDF
    full_text = extract_text_with_pdfplumber(pdf_path)
    if full_text is None:
        return

    while True:
        search_option = input(
            "\nChoose an option:\n"
            "1: Search by professor name\n"
            "2: Search by class name\n"
            "Type 'exit' to quit: ").strip()

        if search_option.lower() == 'exit':
            print("Exiting program. Goodbye!")
            break
        elif search_option == "1":
            search_by_professor(full_text)
        elif search_option == "2":
            search_by_class(full_text)
        else:
            print("Invalid option. Please enter 1, 2, or 'exit'.")

# Run the program
if __name__ == "__main__":
    main()
