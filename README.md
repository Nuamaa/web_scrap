Cause List scraper
Fetches daily cause list from the website in real-time and generates a clean, formatted PDF report.
This project was created as part of the Think Act Rise Foundation - Python Development Internship Task.

# Features
- Fetches real-time cause list data from the Gujarat High Court API
- Automatically generates a PDF with court name, code, and judges
- Fully console-based, no manual web navigation needed

# Libraries used
- requests : for making HTTP POST requests to the High Court API
- fpdf : for creating and formatting the PDF
- datetime : for parsing and formatting the user-input date

# To Run
Install the required libraries:
   ```bash
   pip install requests fpdf

python web_scrap.py