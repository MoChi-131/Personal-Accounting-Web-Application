from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
import datetime
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta
import imghdr
import os
import magic

from MongoDB import Out_monthly, retrieve_expense_data, budget_data, \
    write_Budget, update_Budget
from Graphs import draw_pie_chart, draw_T2_chart, create_expense_plot, sankey
from Save_Data import Save_BS, Save_Reciept
from initial import start

current_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize MongoDB connection
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
except Exception as e:
    print("MongoDB connection error:", e)


# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.pdf']
app.config['UPLOAD_PATH'] = os.path.join(current_dir, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)


# Date setup
categories = ["toll", "food", "parking", "transport", "accommodation", "shopping", "telecom", "miscellaneous", "other"]
upload_path = ""
today= datetime.datetime(2025, 4, 30) # choose the date here
#today = datetime.datetime.now()
next_month = today + relativedelta(months=1)
next_month_date = next_month.strftime("%Y-%m")


# Load budget or initialize default
file_path = os.path.join(current_dir, 'MongoDB','Budget_data', f"budget_{next_month_date}.json")        
if os.path.exists(file_path):
    user_budget = list(budget_data(next_month_date).values())
else:
    user_budget = [1500, 250, 200, 300, 100, 150, 300, 100, 50, 200, 250, 100]

    
# Perform initial setup
start()


@app.route("/", methods=["GET", "POST"])
# Login route: redirects to user's home page
def login():
    if request.method == "POST":
        username = request.form.get("username")
        return redirect(url_for("home", username=username))
    return render_template("login.html")


@app.route("/<username>")
# Home dashboard: show current income, expenses, and budget summary
def home(username):
    current_month = today.strftime("%Y-%m")
    total_expense = round(Out_monthly(current_month), 2)
    this_month_budget = budget_data(current_month)
    total_income = round(this_month_budget["Wadge"] + this_month_budget["Other_Income"],2)

    
    if this_month_budget != 0:
        available_budget = round((sum(this_month_budget.values()) - total_expense - this_month_budget["Wadge"] - this_month_budget["Other_Income"] - this_month_budget["Saving"]), 2)
    else:
        available_budget = 0
    
    draw_pie_chart(current_month, categories)

    return render_template("Dashboard.html", username=username, date=today, income=total_income, expense=total_expense, budget=available_budget)


@app.route("/<username>/Trend_1", methods=["GET", "POST"])
# Trend analysis by time and category
def trend_1(username):
    if request.method == "POST":
        mode = request.form.get('time_period')
        sort = request.form.get('category')
        create_expense_plot(today, mode, categories, sort)
        
    else:
        mode = "Monthly"
        sort = "All Category"
        create_expense_plot(today, mode, categories, sort)
        
    return render_template("Trend_1.html", username=username, categories=categories)


@app.route("/<username>/Trend_2")
# Compare last month's budget vs expenses
def trend_2(username):
    last_month = today - relativedelta(months=1)
    date = last_month.strftime("%B")
    chart_data = retrieve_expense_data(today, categories)
    budget = list(budget_data(last_month.strftime("%Y-%m")).values())
    budget = budget[2:]
    print(budget)

    chart_data = draw_T2_chart(today, budget, categories)
    T2_categories = ["Toll", "Food", "Parking", "Transport", "Accommodation", "Shopping", "Telecom", "Miscellaneous", "Other", "Saving"]
       
    return render_template("Trend_2.html", username=username, date=date, chart_data = chart_data, categories= T2_categories, budget = budget)


@app.route("/<username>/Budget",  methods=["GET", "POST"])
# Set or update budget for next month
def budget(username):

    global next_month
    date = next_month.strftime("%B")
    global user_budget
    income = [user_budget[0], user_budget[1]]
    
    if request.method == "POST":
        wadge = float(request.form.get("wadge", 0))
        other = float(request.form.get("other", 0))
        income = [wadge, other]

        expenses = []
        for i in range(len(categories)): 
            val = request.form.get(f'expense_{i}', 0)
            expenses.append(float(val))

        saving = float(request.form.get("saving", 0))

        # Reconstruct full budget list
        new_budget = [wadge, other] + expenses + [saving]
        
        month = next_month.strftime("%Y-%m")
        
        if os.path.exists(file_path):
            update_Budget(month, new_budget, file_path)
            print("Enter")
        else:
            write_Budget(month, new_budget, file_path)
            
        sankey(new_budget)
        user_budget= new_budget
        print("Updated Budget:", user_budget)
        
    else:
        sankey(user_budget)

    return render_template("Budget.html", username=username, date=date, budget = user_budget, categories=categories, income = income)
    
    
def validate_file(stream, file_ext):
    # Validate uploaded file format
    
    # Reset stream position after reading
    stream.seek(0)
    
    # For image extensions (.jpg, .png), validate using imghdr
    if file_ext in ['.jpg', '.png']:
        header = stream.read(512)
        stream.seek(0)
        format = imghdr.what(None, header)
        if not format:
            return False
        return file_ext == ('.' + (format if format != 'jpeg' else 'jpg'))
    
    # For PDF, use python-magic to check MIME type
    if file_ext == '.pdf':
        header = stream.read(512)
        stream.seek(0)
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(header)
        return file_type == 'application/pdf'
    
    return False

@app.errorhandler(413)
# Handle large file error
def too_large(e):
    return "File is too large", 413


@app.route("/<username>/Upload", methods=["GET", "POST"])
# Upload page for receipts and bank statements
def upload_page(username):
    files = os.listdir(app.config['UPLOAD_PATH'])

    if request.method == "POST":
        print("Here")
        category = request.form.get("category")  # Use form not get_data

        global upload_path 
        if category == "bank":
            Save_BS(upload_path)
        else:
            Save_Reciept(upload_path)


        return render_template("Upload.html", username=username, files=files)

    return render_template("Upload.html", username=username, files=files)


@app.route('/Upload', methods=['POST'])
# File upload handler
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
            
    if filename != '':
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "File extension not allowed", 400
        if not validate_file(uploaded_file.stream, file_ext):
            return "Invalid file format", 400
        global upload_path 
        upload_path= os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(upload_path)
                
    return '', 204

@app.route('/uploads/<filename>')
# Serve uploaded files
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


# Run the app
if __name__ == "__main__":
    app.run(debug=False)
