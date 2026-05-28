import re

file_path = "blog/he/pt-web-registration-diagnostic.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

update_text = """
    <h2>עדכון מאוחר (Post-Mortem: מאי 2026)</h2>
    <p>במבט לאחור, התובנה הראשונית שלי לגבי ה"קריסה" הייתה חלקית. כשהרצתי את השאילתה מול ה-API בזמן אמת (לאחר פתיחת ההרשמה הרשמית), גיליתי שהמערכת מעולם לא קרסה – היא פשוט עבדה לפי <em>State Machine</em> נוקשה. ה-"0 Lotteries" שראיתי בתחילת אפריל לא נבעו מ-DB נעול, אלא מהעובדה שהנתונים החדשים פשוט טרם שוחררו ל-Public API. הלקח המרכזי כאן עבורי כחוקר הוא שלפעמים "חוסר נתונים" הוא התנהגות מתוכננת של ה-Backend, ולאו דווקא תקלה ב-Frontend. כעת, כשההרשמה פתוחה, ה-API מחזיר את כל הנתונים המלאים – מה שמוכיח שהארכיטקטורה עמידה ומתפקדת היטב.</p>
"""

# מחליפים את ה"שורה התחתונה" הישנה בעדכון החדש
new_content = re.sub(r"<h2>השורה התחתונה: ארכיטקטורה מול מציאות</h2>.*", update_text, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
