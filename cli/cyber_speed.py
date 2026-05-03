#!/usr/bin/env python3

import speedtest
from datetime import datetime
import os, sys, random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import matplotlib.pyplot as plt

TOOL_NAME = "ISS"
GITHUB = "github.com/surya404root"

# ---------- UI ----------
def banner():
    os.system("clear")
    print("\033[1;32m")
    print("""
██╗███████╗███████╗
██║██╔════╝██╔════╝
██║███████╗███████╗
██║╚════██║╚════██║
██║███████║███████║
╚═╝╚══════╝╚══════╝
""")
    print("⚡ ISS - Internet Speed Scanner ⚡")
    print("\033[0m")

# ---------- SPEED TEST ----------
def run_test():
    st = speedtest.Speedtest()
    st.get_best_server()

    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    ping = st.results.ping

    res = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ping": ping,
        "download": download,
        "upload": upload
    }

    print("\n📊 RESULTS")
    print(f"Ping: {ping:.2f} ms")
    print(f"Download: {download:.2f} Mbps")
    print(f"Upload: {upload:.2f} Mbps")

    return res

# ---------- GRAPH ----------
def create_chart(res):
    plt.figure()
    plt.bar(["Download", "Upload"], [res['download'], res['upload']])
    plt.title("Speed Test")
    plt.savefig("chart.png")
    plt.close()

# ---------- PDF ----------
def draw_background(c, w, h):
    c.setFillColorRGB(0,0,0)
    c.rect(0,0,w,h,fill=1)

    c.setFillColorRGB(0,0.5,0)
    for _ in range(80):
        c.drawString(random.randint(0,int(w)), random.randint(0,int(h)), random.choice("01"))

    c.setFont("Courier", 30)
    c.drawCentredString(w/2, h/2, TOOL_NAME)

    c.setFont("Courier", 10)
    c.drawCentredString(w/2, 20, GITHUB)

def generate_pdf(res):
    os.makedirs("reports", exist_ok=True)

    file_name = f"reports/ISS_Report_{res['time'].replace(':','-').replace(' ','_')}.pdf"

    create_chart(res)

    doc = SimpleDocTemplate(file_name, pagesize=letter)
    styles = getSampleStyleSheet()

    hacker = ParagraphStyle(
        'hacker', parent=styles['Normal'],
        fontName="Courier", fontSize=10,
        textColor=colors.green
    )

    content = []

    content.append(Paragraph("ISS - Internet Speed Scanner", hacker))
    content.append(Spacer(1,15))

    for k,v in res.items():
        content.append(Paragraph(f"{k}: {v}", hacker))
        content.append(Spacer(1,10))

    if os.path.exists("chart.png"):
        content.append(Image("chart.png", width=400, height=200))

    def bg(canvas, doc):
        draw_background(canvas, *letter)

    doc.build(content, onFirstPage=bg)

    print(f"📄 PDF saved: {file_name}")

# ---------- MAIN ----------
def main():
    banner()
    res = run_test()

    while True:
        print("\n1. Save PDF")
        print("2. Open Web Test")
        print("0. Exit")

        c = input("Choice: ")

        if c == "1":
            generate_pdf(res)
        elif c == "2":
            os.system("termux-open-url https://fast.com")
        else:
            sys.exit()

if __name__ == "__main__":
    main()
