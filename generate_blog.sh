#!/bin/bash

echo "Starting Blog Refactoring..."

# א. ניקוי הסרגל הצידי מכל המאמרים
for file in blog/he/*.html; do
    if [ -f "$file" ]; then
        sed -i '/id="sidebar"/d' "$file"
    fi
done

# ב. בניית שלד ה-HTML לעמוד הבלוג המרכזי
HUB_HTML="<!DOCTYPE html>
<html lang=\"he\" dir=\"rtl\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>המאמרים שלי | שי מרדכי</title>
    <link rel=\"stylesheet\" href=\"../../assets/css/style.css\">
    <style>
        body { background-color: var(--bg-color); color: var(--text-color); font-family: system-ui, -apple-system, sans-serif; }
        #content { margin: 0 auto; max-width: 800px; padding: 40px; }
        .article-card { background: var(--sidebar-bg); padding: 25px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px; transition: transform 0.2s, border-color 0.2s; display: block; text-decoration: none;}
        .article-card:hover { transform: translateY(-3px); border-color: var(--accent-color); text-decoration: none; }
        .article-title { font-size: 1.4rem; font-weight: bold; color: var(--accent-color); margin-bottom: 10px; display: block;}
        .article-date { color: #8b949e; font-size: 0.95rem; }
        .back-btn { color: var(--accent-color); text-decoration: none; font-weight: bold; display: inline-block; margin-bottom: 30px; font-size: 1.1rem; }
        .back-btn:hover { text-decoration: underline; }
    </style>
</head>
<body>
<div id=\"content\">
    <a href=\"../../index.html\" class=\"back-btn\">← חזרה לתיק העבודות (Home)</a>
    <h1 style=\"border-bottom: 2px solid #334155; padding-bottom: 15px; margin-bottom: 30px;\">מחקרים ומאמרים טכניים</h1>
    <div style=\"display: flex; flex-direction: column; gap: 15px;\">"

# ג. סריקת המאמרים ויצירת הכרטיסיות
# שימוש ב-ls -t כדי למיין מהחדש לישן
for file in $(ls -t blog/he/*.html); do
    filename=$(basename "$file")
    if [ "$filename" == "index.html" ]; then continue; fi
    
    # חילוץ כותרת
    title=$(grep -oP '(?<=<h1>).*?(?=</h1>)' "$file" | head -n 1)
    if [ -z "$title" ]; then title=$filename; fi
    
    # חילוץ תאריך בצורה חכמה יותר (מחלץ כל מה שבתוך ה-em הראשון אחרי הכותרת)
    date_line=$(grep -oP '(?<=<em>).*?(?=</em>)' "$file" | head -n 1)
    if [ -z "$date_line" ]; then date_line="תאריך פרסום יתווסף בקרוב"; fi
    
    # הוספת כרטיסייה ל-Hub (עכשיו כל הכרטיסייה לחיצה)
    HUB_HTML+="<a href=\"${filename}\" class=\"article-card\">"
    HUB_HTML+="<span class=\"article-title\">${title}</span>"
    HUB_HTML+="<span class=\"article-date\">${date_line}</span>"
    HUB_HTML+="</a>"
    
    # הוספת כפתור "חזרה לבלוג" לתוך המאמר עצמו
    BACK_LINK='<a href="index.html" style="color: var(--accent-color); text-decoration: none; font-weight: bold; display: inline-block; margin-bottom: 20px; font-size: 1.1rem;">← חזרה לרשימת המאמרים</a>'
    if ! grep -q "חזרה לרשימת המאמרים" "$file"; then
        sed -i "s|<div id=\"content\">|<div id=\"content\">\n    ${BACK_LINK}|" "$file"
    fi
done

HUB_HTML+="</div></div></body></html>"

# שמירת עמוד ה-Hub החדש
echo "$HUB_HTML" > blog/he/index.html
echo "Blog generation successfully completed with dates!"
