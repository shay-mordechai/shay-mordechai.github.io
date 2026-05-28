# scripts/generate_hub.py
import os, re

DIR = 'blog/he'
OUTPUT = 'blog/he/index.html'

CATEGORIES = {
    "Projects": ["sniper", "diagnostics", "architecture", "registration", "mitigation", "saas", "trading", "compiler", "zero-day", "firewall", "myleads"],
    "Articles": ["android", "browser", "paradox", "jni", "rust", "v8", "kinoite", "malware", "routing"],
    "Writeups": ["uncrackable"]
}

HEBREW_MONTHS = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"]

def parse_and_format_date(date_str):
    """ממיר כל פורמט תאריך לפורמט עברי אחיד ולמספרים לטובת מיון"""
    date_str_lower = date_str.lower()
    year, month, day = 1970, 1, 1

    months_heb_map = {"ינואר": 1, "בינואר": 1, "פברואר": 2, "בפברואר": 2, "מרץ": 3, "במרץ": 3, "אפריל": 4, "באפריל": 4, "מאי": 5, "במאי": 5, "יוני": 6, "ביוני": 6, "יולי": 7, "ביולי": 7, "אוגוסט": 8, "באוגוסט": 8, "ספטמבר": 9, "בספטמבר": 9, "אוקטובר": 10, "באוקטובר": 10, "נובמבר": 11, "בנובמבר": 11, "דצמבר": 12, "בדצמבר": 12}
    months_eng_map = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}

    # חיפוש תאריך בעברית
    m_heb = re.search(r'(\d{1,2})\s+([א-ת]+)\s+(\d{4})', date_str)
    # חיפוש תאריך באנגלית
    m_eng = re.search(r'([a-z]+)\s+(\d{1,2}),?\s+(\d{4})', date_str_lower)

    if "31 ביולי 2025" in date_str or "בקרוב" in date_str:
        return "31 ביולי 2025", (2025, 7, 31)
    elif m_heb:
        day = int(m_heb.group(1))
        month = months_heb_map.get(m_heb.group(2), 1)
        year = int(m_heb.group(3))
    elif m_eng:
        month = months_eng_map.get(m_eng.group(1), 1)
        day = int(m_eng.group(2))
        year = int(m_eng.group(3))
    else:
        return "תאריך לא ידוע", (1970, 1, 1)

    formatted_date = f"{day} ב{HEBREW_MONTHS[month-1]} {year}"
    return formatted_date, (year, month, day)

def extract_clean_excerpt(content):
    """שולף תקציר תוך דילוג על שורות קרדיט (מאת / By)"""
    paragraphs = re.findall(r'<p>(.*?)</p>', content, re.DOTALL)
    for p in paragraphs:
        text = re.sub(r'<[^>]+>', '', p).strip() # ניקוי HTML
        # דילוג על פסקאות קצרות שמכילות מידע מטא
        if len(text) < 100 and any(x in text.lower() for x in ["מאת", "by ", "תאריך", "סטטוס"]):
            continue
        if len(text) > 20: # מצאנו את פסקת התוכן האמיתית הראשונה
            return text[:90] + "..." if len(text) > 90 else text
    return ""

def get_category(title):
    title_l = title.lower()
    for cat, keywords in CATEGORIES.items():
        if any(key in title_l for key in keywords):
            return cat
    return "Articles" # Default

data = {"Projects": [], "Articles": [], "Writeups": []}

for filename in os.listdir(DIR):
    if filename in ['index.html', '..'] or not filename.endswith('.html'): continue
    path = os.path.join(DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

        title_match = re.search(r'<h1>(.*?)</h1>', content)
        title = title_match.group(1).strip() if title_match else filename

        date_match = re.search(r'<em>(.*?)</em>', content)
        raw_date = date_match.group(1).strip() if date_match else ""
        formatted_date, sort_tuple = parse_and_format_date(raw_date)

        excerpt = extract_clean_excerpt(content)
        cat = get_category(title)

        data[cat].append({
            'file': filename,
            'title': title,
            'date': formatted_date,
            'sort_key': sort_tuple,
            'excerpt': excerpt
        })

# מיון לפי תאריך (החדש ביותר למעלה)
for cat in data:
    data[cat].sort(key=lambda x: x['sort_key'], reverse=True)

# בניית ה-HTML
html = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="../../assets/css/style.css">
    <title>מאגר המאמרים והפרויקטים של שי מרדכי</title>
    <style>
        .categories-container { display: flex; gap: 25px; align-items: flex-start; justify-content: space-between; max-width: 1400px; margin: 0 auto; padding: 20px; }
        .category-column { flex: 1; min-width: 300px; display: flex; flex-direction: column; gap: 15px; }
        .category-column h2 { border-bottom: 2px solid #30363d; padding-bottom: 10px; color: #c9d1d9; font-size: 1.5rem; }
        .article-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 16px; text-decoration: none; width: 100%; box-sizing: border-box; display: flex; flex-direction: column; transition: border-color 0.2s, transform 0.2s; }
        .article-card:hover { border-color: #8b949e; transform: translateY(-2px); }
        @media (max-width: 900px) { .categories-container { flex-direction: column; } }
    </style>
</head>
<body>
<div id="content" style="max-width: 100%; padding:0;">
    <h1 style="text-align: center; margin: 40px 0;">מאגר הפרויקטים והמחקרים</h1>
    <div class="categories-container">
"""

for cat in ["Projects", "Articles", "Writeups"]:
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
