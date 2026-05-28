import os, re

# הגדרות
DIR = 'blog/he'
OUTPUT = 'blog/he/index.html'

# מיפוי חודשים למיון
months = {'ינואר': '01', 'פברואר': '02', 'מרץ': '03', 'אפריל': '04', 'מאי': '05', 'יוני': '06', 
          'יולי': '07', 'אוגוסט': '08', 'ספטמבר': '09', 'אוקטובר': '10', 'נובמבר': '11', 'דצמבר': '12'}

def get_sort_key(date_str):
    match = re.search(r'(\d{1,2}) ב([א-ת]+) (\d{4})', date_str)
    if match:
        day, month_word, year = match.groups()
        return f"{year}-{months.get(month_word, '00')}-{int(day):02d}"
    return "1970-01-01"

# קטגוריות
data = {"Research": [], "Project": [], "Writeup": []}

for filename in os.listdir(DIR):
    if filename == 'index.html' or not filename.endswith('.html'): continue
    path = os.path.join(DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # חילוץ נתונים
        title = re.search(r'<h1>(.*?)</h1>', content)
        title = title.group(1).strip() if title else filename
        
        date_match = re.search(r'<em>.*?(\d{1,2} ב[א-ת]+ \d{4}).*?</em>', content)
        date_str = date_match.group(1) if date_match else "תאריך יתווסף"
        
        # זיהוי קטגוריה
        cat = "Research"
        if "UnCrackable" in title or "Writeup" in title: cat = "Writeup"
        elif "Project" in title or "בוט מסחר" in title or "Firewall" in title or "MyLeads" in title: cat = "Project"
        
        # תקציר נקי
        excerpt = re.search(r'<p>(.*?)</p>', content, re.DOTALL)
        excerpt = re.sub('<[^<]+?>', '', excerpt.group(1)).strip()[:120] + "..." if excerpt else ""
        
        data[cat].append({'file': filename, 'title': title, 'date': date_str, 'sort_key': get_sort_key(date_str), 'excerpt': excerpt})

# בניית ה-HTML
html = f"""<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="UTF-8">
<link rel="stylesheet" href="../../assets/css/style.css">
<style>
    body {{ background-color: var(--bg-color); color: var(--text-color); font-family: system-ui, sans-serif; }}
    #content {{ margin: 0 auto; max-width: 1200px; padding: 40px; }}
    .grid {{ display: flex; gap: 20px; align-items: flex-start; flex-wrap: wrap; }}
    .column {{ flex: 1; min-width: 300px; }}
    .article-card {{ background: var(--sidebar-bg); padding: 20px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 15px; display: block; text-decoration: none; }}
    .article-card:hover {{ border-color: var(--accent-color); }}
    h3 {{ color: var(--accent-color); border-bottom: 2px solid var(--accent-blue); padding-bottom: 10px; }}
</style>
</head><body><div id="content">
<a href="../../index.html" style="color:var(--accent-blue); display:block; margin-bottom:20px;">← חזרה לתיק העבודות</a>
<h1>מאגר ידע (Knowledge Vault)</h1>
<div class="grid">"""

for cat_key, cat_name in [("Research", "מחקרים ומאמרים"), ("Project", "פרויקטים"), ("Writeup", "אתגרי אבטחה")]:
    html += f"<div class='column'><h3>{cat_name}</h3>"
    sorted_arts = sorted(data[cat_key], key=lambda x: x['sort_key'], reverse=True)
    for art in sorted_arts:
        html += f"""<a href="{art['file']}" class="article-card">
            <div style="font-weight:bold; color:#fff;">{art['title']}</div>
            <div style="font-size:0.8rem; color:#8b949e;">{art['date']}</div>
            <div style="font-size:0.9rem; margin-top:5px;">{art['excerpt']}</div>
        </a>"""
    html += "</div>"

html += "</div></div></body></html>"
with open(OUTPUT, 'w', encoding='utf-8') as f: f.write(html)
