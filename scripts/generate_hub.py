import os, re

DIR = 'blog/he'
OUTPUT = 'blog/he/index.html'

def parse_hebrew_date(date_str):
    """ממיר תאריך בעברית לטאפל של (שנה, חודש, יום) לטובת מיון"""
    months = {
        "ינואר": 1, "בינואר": 1, "פברואר": 2, "בפברואר": 2, "מרץ": 3, "במרץ": 3,
        "אפריל": 4, "באפריל": 4, "מאי": 5, "במאי": 5, "יוני": 6, "ביוני": 6,
        "יולי": 7, "ביולי": 7, "אוגוסט": 8, "באוגוסט": 8, "ספטמבר": 9, "בספטמבר": 9,
        "אוקטובר": 10, "באוקטובר": 10, "נובמבר": 11, "בנובמבר": 11, "דצמבר": 12, "בדצמבר": 12
    }
    m = re.search(r'(\d{1,2})\s+([א-ת]+)\s+(\d{4})', date_str)
    if m:
        day = int(m.group(1))
        month_name = m.group(2)
        year = int(m.group(3))
        month = months.get(month_name, 1)
        return (year, month, day)
    return (1970, 1, 1) # ברירת מחדל אם אין תאריך

data = {"Projects": [], "Research": [], "Writeups": []}

for filename in os.listdir(DIR):
    if filename in ['index.html', '..'] or not filename.endswith('.html'): continue
    path = os.path.join(DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # חילוץ כותרת
        title_match = re.search(r'<h1>(.*?)</h1>', content)
        title = title_match.group(1).strip() if title_match else filename
        
        # חילוץ תאריך
        date_match = re.search(r'<em>.*?\|\s*(.*?)</em>', content)
        date_str = date_match.group(1).strip() if date_match else "תאריך לא ידוע"
        
        # חילוץ תקציר
        excerpt_match = re.search(r'<p>(.*?)</p>', content, re.DOTALL)
        if excerpt_match and "מאת שי מרדכי" in excerpt_match.group(1):
            paragraphs = re.findall(r'<p>(.*?)</p>', content, re.DOTALL)
            excerpt = paragraphs[1] if len(paragraphs) > 1 else excerpt_match.group(1)
        else:
            excerpt = excerpt_match.group(1) if excerpt_match else ""
        
        excerpt = re.sub(r'<[^>]+>', '', excerpt)
        excerpt_short = excerpt[:80] + "..." if len(excerpt) > 80 else excerpt

        # סיווג
        cat = "Research"
        title_lower = title.lower()
        project_keywords = ["sniper", "zero-day", "compiler", "project", "firewall", "myleads", "diagnostics", "mitigation", "trading", "saas"]
        if any(x in title_lower for x in project_keywords):
            cat = "Projects"
        elif "uncrackable" in title_lower or "writeup" in title_lower:
            cat = "Writeups"

        data[cat].append({
            'file': filename, 
            'title': title,
            'date': date_str,
            'excerpt': excerpt_short
        })

# מיון כל קטגוריה מהחדש לישן
for cat in data:
    data[cat].sort(key=lambda x: parse_hebrew_date(x['date']), reverse=True)

# הרכבת ה-HTML
html = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../../assets/css/style.css">
    <title>מאגר המאמרים והפרויקטים של שי מרדכי</title>
    <style>
        /* מבנה של עמודות במקביל */
        .categories-container {
            display: flex;
            gap: 25px;
            align-items: flex-start;
            justify-content: space-between;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .category-column {
            flex: 1;
            min-width: 300px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .category-column h2 {
            border-bottom: 2px solid #30363d;
            padding-bottom: 10px;
            color: #c9d1d9;
            font-size: 1.5rem;
        }
        .article-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 16px;
            text-decoration: none;
            width: 100%;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            transition: border-color 0.2s, transform 0.2s;
        }
        .article-card:hover { 
            border-color: #8b949e; 
            transform: translateY(-2px);
        }
        /* תאימות למובייל - העמודות ירדו אחת מתחת לשניה במסכים קטנים */
        @media (max-width: 900px) {
            .categories-container { flex-direction: column; }
        }
    </style>
</head>
<body>
<div id="content" style="max-width: 100%; padding:0;">
    <h1 style="text-align: center; margin: 40px 0;">מאגר הפרויקטים והמחקרים</h1>
    <div class="categories-container">
"""

for cat in ["Projects", "Research", "Writeups"]:
    if not data[cat]: continue
    html += f"<div class='category-column'><h2>{cat}</h2>"
    for item in data[cat]:
        html += f"""
        <a href="{item['file']}" class="article-card">
            <div style="font-weight:bold; color:#fff; font-size:1.1rem;">{item['title']}</div>
            <div style="font-size:0.8rem; color:#8b949e; margin-top:5px; font-family: monospace;">{item['date']}</div>
            <div style="font-size:0.9rem; margin-top:10px; color:#8b949e; line-height:1.4;">{item['excerpt']}</div>
        </a>"""
    html += "</div>"

html += "</div></div></body></html>"

with open(OUTPUT, 'w', encoding='utf-8') as f: f.write(html)
