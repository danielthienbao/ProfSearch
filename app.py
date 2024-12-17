from flask import Flask, request, render_template
from app.utils import extract_text_with_pdfplumber, search_by_professor, search_by_class

app = Flask(__name__)
PDF_PATH = "uploads/SuccCompletion_Sp24_Instruct.pdf"

# Load the PDF text at startup
full_text = extract_text_with_pdfplumber(PDF_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    result_table = None
    search_type = None
    search_query = None

    if request.method == "POST":
        search_type = request.form.get("search_type")
        search_query = request.form.get("query").strip()

        if search_type == "professor":
            result_table = search_by_professor(full_text, search_query)
        elif search_type == "class":
            result_table = search_by_class(full_text, search_query)

        return render_template("results.html", results=result_table, query=search_query, search_type=search_type)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
