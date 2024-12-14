# to run: python professor_stat.py
import re
from PyPDF2 import PdfReader
from tabulate import tabulate

def extract_professor_stats(pdf_path):
    # Read the PDF
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()

    # Loop to allow repeated searches
    while True:
        name_query = input("\nEnter the professor's first name, last name, or both (or type 'exit' to quit): ").strip()
        if name_query.lower() == 'exit':
            print("Exiting program. Goodbye!")
            break

        # Search for the professor's statistics
        matching_lines = []
        lines = full_text.split("\n")
        for line in lines:
            if all(part.lower() in line.lower() for part in name_query.split()):
                matching_lines.append(line)

        # Handle results
        if not matching_lines:
            print(f"No data found for '{name_query}'. Please check the name and try again.")
            continue

        # If multiple matches, ask user to narrow down
        if len(matching_lines) > 1:
            print(f"\nMultiple matches found for '{name_query}'. Please choose one:")
            table_data = []
            for i, line in enumerate(matching_lines, start=1):
                table_data.append([i, line])
            print(tabulate(table_data, headers=["Option", "Professor Details"], tablefmt="grid"))

            try:
                choice = input("\nEnter the number corresponding to the professor or type 'exit' to quit: ").strip()
                if choice.lower() == 'exit':
                    continue
                choice = int(choice) - 1
                if 0 <= choice < len(matching_lines):
                    # Display details in a formatted table
                    display_professor_details(matching_lines[choice])
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please try again.")
        else:
            # Single match found
            display_professor_details(matching_lines[0])

def display_professor_details(professor_line):
    # Extract and format data from the professor's details line
    fields = professor_line.split()
    table_headers = [
        "Division", "Course", "Professor", "Method", "Success Rate (%)", 
        "Completion Rate (%)", "A", "B", "C", "IPP", "D", "F", "INP", "W", "Total"
    ]

    # Adjust based on extracted fields
    data = [fields[:15]]  # Use the first 15 fields for the table
    print("\nStatistics for the selected professor:\n")
    print(tabulate(data, headers=table_headers, tablefmt="grid"))

# Example Usage
pdf_path = "SuccCompletion_Sp24_Instruct.pdf"  # Path to your PDF file
extract_professor_stats(pdf_path)
