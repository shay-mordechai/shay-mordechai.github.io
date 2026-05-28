#!/bin/bash

echo "Starting Blog Refactoring with Chronological Sorting..."

# פונקציית עזר להמרת חודש עברי למספר לטובת מיון
get_month_num() {
    case "$1" in
        *"ינואר"*) echo "01" ;;
        *"פברואר"*) echo "02" ;;
        *"מרץ"*) echo "03" ;;
        *"אפריל"*) echo "04" ;;
        *"מאי"*) echo "05" ;;
        *"יוני"*) echo "06" ;;
        *"יולי"*) echo "07" ;;
        *"אוגוסט"*) echo "08" ;;
        *"ספטמבר"*) echo "09" ;;
        *"אוקטובר"*) echo "10" ;;
        *"נובמבר"*) echo "11" ;;
        *"דצמבר"*) echo "12" ;;
        *) echo "00" ;;
    esac
}

# הסרת סרגל צדדי ישן
for file in blog/he/*.html; do
    if [ -f "$file" ]; then
        sed -i '/id="sidebar"/d' "$file"
    fi
done

HUB_HTML="<!DOCTYPE html>
<html lang=\"he\" dir=\"rtl\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>המאמרים שלי | שי מרדכי</title>
    <link rel=\"stylesheet\" href=\"../../assets/css/style.css\">
    <style>
        body { background-color: var(--bg-color); color: var(--text-color); font-family: system-ui, -apple-system, sans-serif; }
        #content { margin: 0 auto; max-width: 850px; padding: 40px; }
        .article-card { background: var(--sidebar-bg); padding: 25px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px; transition: transform 0.2s, border-color 0.2s; display: block; text-decoration: none; position: relative;}
        .article-card:hover { transform: translateY(-3px); border-color: var(--accent-color); text-decoration: none; }
        .article-title { font-size: 1.4rem; font-weight: bold; color: var(--accent-color); margin-bottom: 5px; display: block; padding-top: 15px;}
        .article-date { color: #8b949e; font-size: 0.9rem; margin-bottom: 15px; display: block; }
        .article-excerpt { color: var(--text-color); font-size: 1rem; line-height: 1.5; display: block;}
        .badge { position: absolute; top: 20px; right: 25px; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; font-family: 'JetBrains Mono', monospace; }
        .back-btn { color: var(--accent-color); text-decoration: none; font-weight: bold; display: inline-block; margin-bottom: 30px; font-size: 1.1rem; }
        .back-btn:hover { text-decoration: underline; }
    </style>
</head>
<body>
<div id=\"content\">
    <a href=\"../../index.html\" class=\"back-btn\">← חזרה לתיק העבודות (Home)</a>
    <h1 style=\"border-bottom: 2px solid #334155; padding-bottom: 15px; margin-bottom: 30px;\">מחקרים, מאמרים ופרויקטים</h1>
    <div style=\"display: flex; flex-direction: column; gap: 15px;\">"

# קובץ זמני לאחסון המידע לשם מיון
> tmp_sort.txt

for file in blog/he/*.html; do
    filename=$(basename "$file")
    if [ "$filename" == "index.html" ]; then continue; fi
    
    title=$(grep -oP '(?<=<h1>).*?(?=</h1>)' "$file" | head -n 1)
    if [ -z "$title" ]; then title=$filename; fi
    
    date_line=$(grep -oP '(?<=<em>).*?(?=</em>)' "$file" | head -n 1)
    if [ -z "$date_line" ]; then date_line="תאריך פרסום יתווסף בקרוב"; fi
    
    excerpt=$(grep -oP '(?<=<p>).*?(?=</p>)' "$file" | grep -v 'מאת שי מרדכי' | head -n 1 | sed 's/<[^>]*>//g')
    excerpt="${excerpt:0:160}..."
    
    # חילוץ תאריך ליצירת מפתח מיון (Sort Key) מפורמט YYYY-MM-DD
    day=$(echo "$date_line" | grep -oP '\b\d{1,2}\b' | head -n 1)
    month_word=$(echo "$date_line" | grep -oP '\bב?[א-ת]+\b' | grep -E 'ינואר|פברואר|מרץ|אפריל|מאי|יוני|יולי|אוגוסט|ספטמבר|אוקטובר|נובמבר|דצמבר' | head -n 1)
    year=$(echo "$date_line" | grep -oP '\b20\d{2}\b' | head -n 1)

    if [ -n "$year" ] && [ -n "$month_word" ] && [ -n "$day" ]; then
        month=$(get_month_num "$month_word")
        day=$(printf "%02d" "$day")
        sort_key="${year}-${month}-${day}"
    else
        sort_key="1970-01-01" # אם אין תאריך תקין, ייזרק לתחתית הרשימה
    fi

    # שמירת המידע בקובץ זמני עם מפתח המיון בראש השורה
    echo "${sort_key}|${filename}|${title}|${date_line}|${excerpt}" >> tmp_sort.txt
done

# קריאת הקובץ הזמני כשהוא ממוין בסדר יורד (r-) לפי התאריך
while IFS='|' read -r sort_key filename title date_line excerpt; do
    
    badge_text="Research"
    badge_bg="rgba(88, 166, 255, 0.1)"
    badge_color="var(--accent-blue)"
    
    if [[ "$title" == *"UnCrackable"* || "$title" == *"Writeup"* || "$filename" == *"uncrackable"* ]]; then
        badge_text="Writeup"
        badge_bg="rgba(63, 185, 80, 0.1)"
        badge_color="var(--accent-green)"
    elif [[ "$title" == *"In Process"* || "$title" == *"בוט מסחר"* || "$title" == *"Project"* || "$title" == *"Firewall"* ]]; then
        badge_text="Project"
        badge_bg="rgba(188, 140, 255, 0.1)"
        badge_color="var(--accent-purple)"
    fi
    
    HUB_HTML+="<a href=\"${filename}\" class=\"article-card\">"
    HUB_HTML+="<div class=\"badge\" style=\"background: ${badge_bg}; color: ${badge_color};\">${badge_text}</div>"
    HUB_HTML+="<span class=\"article-title\">${title}</span>"
    HUB_HTML+="<span class=\"article-date\">${date_line}</span>"
    HUB_HTML+="<span class=\"article-excerpt\">${excerpt}</span>"
    HUB_HTML+="</a>"
    
done < <(sort -r tmp_sort.txt)

rm tmp_sort.txt
HUB_HTML+="</div></div></body></html>"

echo "$HUB_HTML" > blog/he/index.html
echo "Blog generation with pure chronological sorting completed!"
