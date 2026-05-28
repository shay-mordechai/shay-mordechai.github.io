file_path = "blog/he/pt-web-registration-diagnostic.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# הוספת הניתוח החדש
new_analysis = """
    <h2>שלב האימות: השוואת נתונים (מאי 2026)</h2>
    <p>חזרתי לבדוק את ה-API לאחר פתיחת ההרשמה הרשמית. הנתונים שחזרו (JSON) אישרו את ההשערה שלי: המערכת עובדת לפי <em>State Machine</em> נוקשה. בעוד שבאפריל המערך היה ריק, כעת ה-API מחזיר את כל נתוני ההגרלה המלאים, כולל שדות שלא היו חשופים ב-UI, כגון <code>HU_CombatReservist_L</code> (מכסות למשרתי מילואים קרביים).</p>
    <p>השליפה הטכנית בוצעה באמצעות cURL והעברה ל-jq, מה שחשף שדות קריטיים המאפשרים לבצע אופטימיזציה של סיכויי הזכייה. המסקנה הטכנית: המערכת לא קרסה באפריל – היא פשוט עבדה במצב Draft, וה-API הגיב בהתאם להרשאות ה-Backend שטרם הופעלו.</p>
    <div style="background: var(--sidebar-bg); padding: 15px; border-left: 4px solid var(--accent-green);">
        <strong>תובנה טכנית:</strong> ה-Frontend היה "עיוור" למידע לא בגלל תקלה, אלא בגלל ניהול הרשאות (Permission Model) ברמת ה-API Gateway. כחוקר, זה לימד אותי שוב: אל תסמוך על מה שה-UI מציג – תמיד תלך ישר ל-Raw Data.
    </div>
"""

# מוסיף את זה לפני סוף הדיב של התוכן
if "עדכון מאוחר" in content:
    new_content = content.replace("<h2>עדכון מאוחר (Post-Mortem: מאי 2026)</h2>", new_analysis)
else:
    new_content = content.replace("</div></body></html>", new_analysis + "</div></body></html>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
