import os, re

DIR = 'blog/he'
OUTPUT = 'blog/he/index.html'

def get_sort_key(date_str):
    # פונקציית מיון פשוטה
    return date_str 

data = {"Research": [], "Project": [], "Writeup": []}

for filename in os.listdir(DIR):
    if filename == 'index.html' or not filename.endswith('.html'): continue
    path = os.path.join(DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        title_match = re.search(r'<h1>(.*?)</h1>', content)
        title = title_match.group(1).strip() if title_match else filename
        
        # לוגיקת סיווג חדשה:
        # פרויקטים: Sniper, Zero-Day, Compiler, Firewall, MyLeads, Diagnostics
        # אתגרים: UnCrackable, Writeup
        cat = "Research"
        if any(x in title for x in ["Sniper", "Zero-Day", "Compiler", "Project", "Firewall", "MyLeads", "Diagnostics"]):
            cat = "Project"
        elif any(x in title for x in ["UnCrackable", "Writeup"]):
            cat = "Writeup"
            
        data[cat].append({'file': filename, 'title': title})

# בניית ה-HTML (מקוצר להמחשה)
html = "<html><body>"
for cat in ["Project", "Research", "Writeup"]:
    html += f"<h2>{cat}</h2>"
    for item in data[cat]:
        html += f"<a href='{item['file']}'>{item['title']}</a><br>"
html += "</body></html>"

with open(OUTPUT, 'w', encoding='utf-8') as f: f.write(html)
