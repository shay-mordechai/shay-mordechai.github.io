#!/bin/bash

echo "Starting Blog Refactoring with Excerpts..."

# Remove old sidebar from all articles
for file in blog/he/*.html; do
    if [ -f "$file" ]; then
        sed -i '/id="sidebar"/d' "$file"
    fi
done

# Build the base HTML for the Central Hub
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

# Scan articles and generate cards (Sorted newest to oldest)
for file in $(ls -t blog/he/*.html); do
    filename=$(basename "$file")
    if [ "$filename" == "index.html" ]; then continue; fi
    
    # Extract Title
    title=$(grep -oP '(?<=<h1>).*?(?=</h1>)' "$file" | head -n 1)
    if [ -z "$title" ]; then title=$filename; fi
    
    # Extract Date
    date_line=$(grep -oP '(?<=<em>).*?(?=</em>)' "$file" | head -n 1)
    if [ -z "$date_line" ]; then date_line="תאריך פרסום יתווסף בקרוב"; fi
    
    # Extract Excerpt (First paragraph without the author name)
    excerpt=$(grep -oP '(?<=<p>).*?(?=</p>)' "$file" | grep -v 'מאת שי מרדכי' | head -n 1 | sed 's/<[^>]*>//g')
    excerpt="${excerpt:0:160}..."
    
    # Dynamic Badge Logic (Project vs Research)
    badge_text="Research"
    badge_bg="rgba(88, 166, 255, 0.1)" # Blue background
    badge_color="var(--accent-blue)"
    
    # Classify as Project if title matches specific keywords
    if [[ "$title" == *"In Process"* || "$title" == *"בוט מסחר"* || "$title" == *"Firewall"* ]]; then
        badge_text="Project"
        badge_bg="rgba(188, 140, 255, 0.1)" # Purple background
        badge_color="var(--accent-purple)"
    fi
    
    # Append card to Hub HTML
    HUB_HTML+="<a href=\"${filename}\" class=\"article-card\">"
    HUB_HTML+="<div class=\"badge\" style=\"background: ${badge_bg}; color: ${badge_color};\">${badge_text}</div>"
    HUB_HTML+="<span class=\"article-title\">${title}</span>"
    HUB_HTML+="<span class=\"article-date\">${date_line}</span>"
    HUB_HTML+="<span class=\"article-excerpt\">${excerpt}</span>"
    HUB_HTML+="</a>"
    
    # Inject 'Back' button inside the article if it does not exist
    BACK_LINK='<a href="index.html" style="color: var(--accent-color); text-decoration: none; font-weight: bold; display: inline-block; margin-bottom: 20px; font-size: 1.1rem;">← חזרה לרשימת המאמרים והפרויקטים</a>'
    if ! grep -q "חזרה לרשימת המאמרים" "$file"; then
        sed -i "s|<div id=\"content\">|<div id=\"content\">\n    ${BACK_LINK}|" "$file"
    fi
done

HUB_HTML+="</div></div></body></html>"

# Save the Hub page
echo "$HUB_HTML" > blog/he/index.html
echo "Blog generation successfully completed!"
