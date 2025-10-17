import requests
from fpdf import FPDF
from datetime import datetime

url = "https://gujarathc-casestatus.nic.in/gujarathc/GetCauseListData"
date_str = input("Enter date (dd/mm/yyyy): ")
date_obj = datetime.strptime(date_str, "%d/%m/%Y")
day = date_obj.strftime("%d/%m/%Y")

payload = {"listingdate": day}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://gujarathc-casestatus.nic.in",
    "Referer": "https://gujarathc-casestatus.nic.in/gujarathc/",
}

session = requests.Session()
response = session.post(url, data=payload, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Gujarat High Court - Cause List ({day})", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(15, 10, "S.No.", 1, 0, "C") 
        pdf.cell(50, 10, "Court Name", 1, 0, "C")
        pdf.cell(20, 10, "Code", 1, 0, "C")
        pdf.cell(80, 10, "Judge(s)", 1, 1, "C")

        pdf.set_font("Arial", "", 11)
        serial = 1
        has_courts = False
        for block in data.get("finaldata", []):
            for c in block.get("courtdata", []):
                has_courts = True
                pdf.cell(15, 8, str(serial), 1, 0, "C")
                pdf.cell(50, 8, c.get("courtname", "N/A"), 1)
                pdf.cell(20, 8, c.get("courtcode", "N/A"), 1)
                pdf.cell(80, 8, c.get("judgeshortname", "N/A"), 1)
                pdf.ln() 
                serial+=1

        if not has_courts:
            for block in data.get("finaldata", []):
                for err in block.get("ERRORS", []):
                    pdf.cell(0, 10, f" {err.get('ERROR','Unknown error')}", ln=True)

        filename = f"cause_list_{day.replace('/', '_')}.pdf"
        pdf.output(filename)
        print(f"\n PDF saved successfully as {filename}!")

    except ValueError:
        print(" Response not JSON — maybe site changed format or blocked bot.")
else:
    print(f" Error: {response.status_code}")
