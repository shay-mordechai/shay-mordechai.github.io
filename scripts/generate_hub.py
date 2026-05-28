# scripts/generate_hub.py
import os, re

DIR = 'blog/he'
OUTPUT = 'blog/he/index.html'

CATEGORIES = {
    "Projects": ["Sniper", "Diagnostics", "Architecture", "Registration", "Mitigation", "SaaS", "Trading"],
    "Research": ["Android", "Compiler", "Browser", "Paradox", "JNI", "Rust", "v8", "Kinoite", "Malware"],
    "Writeups": ["Uncrackable", "Routing"]
}

def get_category(title):
    for cat, keywords in CATEGORIES.items():
        if any(key.lower() in title.lower() for key in keywords):
            return cat
    return "Research"

data = {"Projects": [], "Research": [], "Writeups": []}

for filename in os.listdir(DIR):
    if filename in ['index.html', '..'] or not filename.endswith('.html'): continue
    path = os.path.join(DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        title_match = re.search(r'<h1>(.*?)</h1>', content)
        title = title_match.group(1).strip() if title_match else filename
        cat = get_category(title)
        data[cat].append({'file': filename, 'title': title})

# יצירת ה-HTML עם CSS פנימי (Inline Stylesheet) שמסדר את התצוגה
html = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <link rel='stylesheet' href='../../assets/css/style.css'>
    <title>מאגר המאמרים והפרויקטים של שי מרדכי</title>
    <style>
        /* עיצוב ייעודי לדף האינדקס */
        #content {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        h1.main-title {
            text-align: center;
            margin-bottom: 40px;
            color: #f8f8f2;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            padding-bottom: 20px;
        }
        .category-section {
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 25px 35px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .category-section h2 {
            color: #4ade80; /* ירוק זרחני */
            border-bottom: 1px dashed rgba(255,255,255,0.1);
            padding-bottom: 10px;
            margin-top: 0;
            font-family: monospace;
            text-align: left; /* יישור לשמאל כי המילים באנגלית */
            direction: ltr;
        }
        .category-section ul {
            list-style: none; /* ביטול הנקודות הרגילות */
            padding: 0;
            margin: 15px 0 0 0;
        }
        .category-section li {
            margin: 12px 0;
            padding-right: 20px;
            position: relative;
        }
        /* יצירת סמל (Bullet) טכני לפני כל מאמר */
        .category-section li::before {
            content: "/>";
            color: #4ade80;
            position: absolute;
            right: 0;
            font-family: monospace;
            font-weight: bold;
        }
        .category-section a {
            color: #e2e8f0;
            text-decoration: none;
            font-size: 1.1rem;
            transition: color 0.2s ease, padding-right 0.2s ease;
            display: inline-block;
        }
        .category-section a:hover {
            color: #4ade80;
            padding-right: 5px; /* אפקט תזוזה קטן בריחוף */
        }
    </style>
</head>
<body>
<div id="content">
    <h1 class="main-title">מאגר המאמרים והפרויקטים של שי מרדכי</h1>
"""

for cat in ["Projects", "Research", "Writeups"]:
    html += f"<div class='category-section'><h2>{cat}</h2><ul>"
    for item in data[cat]:
        html += f"<li><a href='{item['file']}'>{item['title']}</a></li>"
    html += "</ul></div>"

html += "</div></body></html>"

with open(OUTPUT, 'w', encoding='utf-8') as f: f.write(html)
