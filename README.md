# CU_FYP - Personal Accounting Web Application

A Flask-based final year project for personal accounting and receipt processing.
The project combines manual budgeting, transaction analysis, charts, and OCR-assisted data extraction.

## Features
- User dashboard for income, expense, and available budget overview
- Budget planning for monthly categories
- Trend analysis with multiple chart views
- Sankey and pie chart visualizations
- Receipt / bank statement upload workflow
- OCR pipeline integration for financial document processing
- MongoDB-backed storage for receipt and budget data

## Repository Structure
- app/: Active Flask application and Python modules
- app/templates/: Jinja templates for UI pages
- app/static/: CSS, generated graphs, and uploaded files
- app/MongoDB/: MongoDB query and data helper modules
- app/OCR/: OCR backend utilities
- app/Graphs/: Plot generation modules
- docs/demo/: Demonstration video(s)
- docs/report/: Dissertation and report artifacts
- docs/design/: Design files and diagrams
- docs/setup/: Setup notes and command snippets

## Demonstration
- Project walkthrough video: [Watch the demonstration](https://liveuclac-my.sharepoint.com/:v:/g/personal/ucabpw4_ucl_ac_uk/IQCuOyuG8e6xSZ_P6ibRJ_XTAe8lhd_iuUsfNZdKMqgDMR8?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=QhIJKo)
> 🔊 Note: The audio in the walkthrough video is low. Please increase your volume when watching.

- ## Prerequisites
- Python 3.10+
- MongoDB server (local or remote)
- Windows PowerShell (commands below are Windows-friendly)

## Quick Start
1. Open terminal in repository root.
2. Move into app folder:
   - `cd app`
3. Create and activate virtual environment:
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
4. Install dependencies:
   - `python -m pip install --upgrade pip`
   - `pip install -r requirements.txt`
5. Start MongoDB:
   - `"C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe" --port 27017 --dbpath="C:\data\db"`
6. (Optional) Set custom MongoDB URI:
   - `set MONGO_URI=mongodb://localhost:27017/`
7. Run Flask app:
   - `python flask_fyp.py`
8. Open browser:
   - `http://127.0.0.1:5000`

## Database Notes
- Expected database name: `Personal_Accounting`
- Main collections used by the project include:
  - `Receipt`
  - `Budget`
- Budget seed files are in:
  - `app/MongoDB/Budget_data/`

## Development Notes
- The active codebase is under `app/`.
- Legacy duplicate folders were removed to keep the repository non-redundant.
- Uploaded files and generated outputs should not be committed.

## Troubleshooting
- If Flask starts but charts are missing, refresh after navigating through trend pages.
- If upload validation fails, ensure files are only `.jpg`, `.png`, or `.pdf` and within size limits.
- If MongoDB connection fails, verify `MONGO_URI` and MongoDB service status.




