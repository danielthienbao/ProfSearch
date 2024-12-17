import pdfplumber
import pandas as pd
import re

def pdf_to_csv(pdf_path, output_csv_path):
    data = []
    last_course = None  # To store the last known course name
    
    # Define column headers
    columns = ["Division Name", "Dept", "Course", "Name", "Meth", "Succ.", "Compl", "A", "B", "C", 
               "IPP", "D", "F", "INP", "W", "Total"]

    # Open the PDF and extract text
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue  # Skip pages with no text
            
            lines = text.split("\n")

            for line in lines:
                # Print the line for debugging
                print(f"DEBUG LINE: {line}")

                # Loosened regex pattern for matching the table rows
                match = re.match(
                    r"^(.*?)\s+([A-Z\-]+)\s+([A-Z0-9\-]+)?\s+([\w\s,]+?)\s+(\bECC\b|\bONLIN\b|\bHYBRD\b|\bHSDUL\b)\s+(\d+%)\s+(\d+%)"
                    r"(?:\s+(\d+))?(?:\s+(\d+))?(?:\s+(\d+))?(?:\s+(\d+))?(?:\s+(\d+))?(?:\s+(\d+))?(?:\s+(\d+))?(?:\s+(\d+))?$", 
                    line
                )
                
                if match:
                    division, dept, course, name, method, succ, compl, a, b, c, ipp, d, f, inp, w, total = match.groups()
                    # If course name is blank, use the last known course
                    if course:
                        last_course = course
                    else:
                        course = last_course
                    
                    # Append the row data
                    data.append([
                        division.strip(), dept, course, name.strip(), method, succ, compl, 
                        a or "-", b or "-", c or "-", ipp or "-", d or "-", f or "-", inp or "-", w or "-", total or "-"
                    ])
    
    # Create a DataFrame and save to CSV
    if data:
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(output_csv_path, index=False)
        print(f"Data successfully saved to '{output_csv_path}'")
    else:
        print("No data extracted from the PDF.")

# File paths
pdf_path = "SuccCompletion_Sp24_Instruct.pdf"  # Input PDF file
output_csv_path = "output_data.csv"            # Output CSV file

# Run the function
pdf_to_csv(pdf_path, output_csv_path)
