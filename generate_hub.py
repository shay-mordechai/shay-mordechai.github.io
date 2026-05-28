import os
import re
from datetime import datetime

# הגדרת תיקיית המאמרים
DIR = 'blog/he'
OUTPUT = 'blog/he/index.html'

def parse_date(date_str):
    months = {'ינואר': '01', 'פברואר': '02', 'מרץ': '03', 'אפריל': '04', 'מאי': '05', 'יוני': '06', 
              'יולי': '07', 'אוגוסט': '08', 'ספטמבר': '09', 'אוקטובר': '10', 'נובמבר': '11', 'דצמבר': '12'}
    try:
        # חילוץ: יום, חודש, שנה
        match = re.search(r'(\d{1,2}) ב([א-ת]+) (\d{4})', date_str)
        if match:
            day, month_word, year = match.groups()
            return f"{year}-{months[month_word]}-{int(day):02d}"
    except: pass
    return "1970-01-01"

articles = []

for filename in os.listdir(DIR):
    if filename == 'index.html' or not filename.endswith('.html'): continue
    
    with open(os.path.join(DIR, filename), 'r', encoding='utf-8') as f:
        content = f.read()
        title = re.search(r'<h1>(.*?)</h1>', content)
        title = title.group(1) if title else filename
        
        date_match = re.search(r'<em>.*?(\d{1,2} ב[א-ת]+ \d{4}).*?</em>', content)
        date_str = date_match.group(1) if date_match else ""
        
        # חילוץ תקציר: הפסקה הראשונה שאינה מכילה את שם הכותב
        paras = re.findall(r'<p>(.*?)</p>', content, re.DOTALL)
        excerpt = ""
        for p in paras:
            if "מאת שי מרדכי" not in p:
                excerpt = re.sub('<[^<]+?>', '', p).strip()[:150] + "..."
                break

        # סיווג
        cat = "Research"
        if "UnCrackable" in title or "Writeup" in title: cat = "Writeup"
        elif "Project" in title or "בוט מסחר" in title or "Firewall" in title or "MyLeads" in title: cat = "Project"
        
        articles.append({'file': filename, 'title': title, 'date': date_str, 'sort_key': parse_date(date_str), 'excerpt': excerpt, 'cat': cat})

# מיון
articles.sort(key=lambda x: x['sort_key'], reverse=True)

# כתיבת ה-HTML
html = f"""<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="UTF-8"><link rel="stylesheet" href="../../assets/css/style.css"><title>הבלוג שלי</title></head><body><div id="content">
<a href="../../index.html" style="color: var(--accent-blue); display:block; margin-bottom:20px;">← חזרה לתיק העבודות</a>
<h1>מאגר ידע (Knowledge Vault)</h1>"""

for cat in ["Research", "Project", "Writeup"]:
    cat_he = {"Research": "מחקרים ומאמרים", "Project": "פרויקטים", "Writeup": "אתגרי אבטחה"}[cat]
    html += f"<h2 style='margin-top:40px; color:#ffffff;'>{cat_he}</h2>"
    for art in [a for a in articles if a['cat'] == cat]:
        html += f"""<a href="{art['file']}" style="display:block; background:var(--sidebar-bg); padding:20px; border-radius:8px; margin-bottom:15px; text-decoration:none; border:1px solid #334155;">
            <span style="display:block; font-size:1.2rem; color:var(--accent-blue); font-weight:bold;">{art['title']}</span>
            <span style="color:#8b949e; font-size:0.85rem;">{art['date']}</span>
            <p style="color:#c9d1d9; font-size:0.95rem; margin-top:10px;">{art['excerpt']}</p>
        </a>"""

html += "</div></body></html>"

with open(OUTPUT, 'w', encoding='utf-8') as f: f.write(html)
