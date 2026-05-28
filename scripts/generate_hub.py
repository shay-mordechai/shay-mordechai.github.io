import os, re

DIR = 'blog/he'
OUTPUT = 'blog/he/index.html'

data = {"Projects": [], "Research": [], "Writeups": []}

for filename in os.listdir(DIR):
    if filename in ['index.html', '..'] or not filename.endswith('.html'): continue
    path = os.path.join(DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # חילוץ הכותרת
        title_match = re.search(r'<h1>(.*?)</h1>', content)
        title = title_match.group(1).strip() if title_match else filename
        
        # חילוץ התאריך
        date_match = re.search(r'<em>.*?\|\s*(.*?)</em>', content)
        date_str = date_match.group(1).strip() if date_match else "תאריך לא ידוע"
        
        # חילוץ תקציר
        excerpt_match = re.search(r'<p>(.*?)</p>', content, re.DOTALL)
        if excerpt_match and "מאת שי מרדכי" in excerpt_match.group(1):
            paragraphs = re.findall(r'<p>(.*?)</p>', content, re.DOTALL)
            excerpt = paragraphs[1] if len(paragraphs) > 1 else excerpt_match.group(1)
        else:
            excerpt = excerpt_match.group(1) if excerpt_match else ""
        
        # ניקוי תגיות HTML מהתקציר
        excerpt = re.sub(r'<[^>]+>', '', excerpt)
        excerpt_short = excerpt[:90] + "..." if len(excerpt) > 90 else excerpt

        # סיווג חכם לפרויקטים, מחקר וכו'
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

# הרכבת ה-HTML במבנה ה-Cards המקורי
html = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../../assets/css/style.css">
    <title>מאגר המאמרים והפרויקטים של שי מרדכי</title>
    <style>
        .articles-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 40px;
        }
        /* מחלקת העיצוב המקורית שהייתה לך */
        .article-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 16px;
            text-decoration: none;
            width: calc(50% - 10px);
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            transition: border-color 0.2s;
        }
        .article-card:hover { border-color: #8b949e; }
        @media (max-width: 768px) { .article-card { width: 100%; } }
    </style>
</head>
<body>
<div id="content">
    <h1>מאגר המאמרים והפרויקטים של שי מרדכי</h1>
"""

for cat in ["Projects", "Research", "Writeups"]:
    if not data[cat]: continue
    html += f"<h2>{cat}</h2><div class='articles-grid'>"
    for item in data[cat]:
        html += f"""
        <a href="{item['file']}" class="article-card">
            <div style="font-weight:bold; color:#fff;">{item['title']}</div>
            <div style="font-size:0.8rem; color:#8b949e; margin-top:5px;">{item['date']}</div>
            <div style="font-size:0.9rem; margin-top:8px; color:#c9d1d9; line-height:1.4;">{item['excerpt']}</div>
        </a>"""
    html += "</div>"

html += "</div></body></html>"

with open(OUTPUT, 'w', encoding='utf-8') as f: f.write(html)
