#!/bin/bash

# בניית ה-HTML לסרגל הצידי מכל הקבצים בתיקייה
SIDEBAR_HTML="<div id=\"sidebar\"><h2>המאמרים שלי</h2><ul>"

for file in blog/he/*.html; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        title=$(grep -oP '(?<=<h1>).*(?=</h1>)' "$file" | head -n 1)
        if [ -z "$title" ]; then
            title=$filename
        fi
        SIDEBAR_HTML="${SIDEBAR_HTML}<li><a href=\"/blog/he/${filename}\">${title}</a></li>"
    fi
done

SIDEBAR_HTML="${SIDEBAR_HTML}</ul></div>"

# הזרקת הסרגל הצידי לכל קובץ (אם טרם הוזרק)
for file in blog/he/*.html; do
    if [ -f "$file" ]; then
        if ! grep -q 'id="sidebar"' "$file"; then
            sed -i "s|<body>|<body>\n${SIDEBAR_HTML}|" "$file"
            echo "Added sidebar to $file"
        fi
    fi
done

echo "Blog generation successfully completed!"
