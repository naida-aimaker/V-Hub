import flet as ft
import os
import json
import gspread

# --- 🔐 НАЛАШТУВАННЯ БЕЗПЕКИ ---
def get_google_sheets():
    try:
        # Важливо: у Vercel використовуйте назву ключа, яку ви задали в налаштуваннях
        creds_json_string = os.environ.get("GOOGLE_CREDENTIALS")
        
        if not creds_json_string:
            print("ПОМИЛКА: Змінна середовища GOOGLE_CREDENTIALS не знайдена!")
            return None
            
        creds_dict = json.loads(creds_json_string)
        # Використовуємо офіційний метод gspread для словника
        return gspread.service_account_from_dict(creds_dict)
    except Exception as e:
        print(f"Помилка ініціалізації Google Sheets: {e}")
        return None

# Ініціалізація клієнта (викликається один раз)
gc = get_google_sheets()

# --- 📊 ЛОГІКА ДАНИХ ---
def get_businesses_from_sheet():
    if not gc:
        return []
    try:
        sh = gc.open("V-Hub_Database")
        worksheet = sh.worksheet("Businesses")
        return worksheet.get_all_records()
    except Exception as e:
        print(f"Критична помилка отримання даних: {e}")
        return []

# --- 🎨 ІНТЕРФЕЙС ---
def create_business_card(name, category, description):
    return ft.Card(
        content=ft.Container(
            padding=15,
            content=ft.Column([
                ft.Text(name, size=18, weight="bold"),
                ft.Text(category, size=12, color="grey"),
                ft.Text(description, size=14),
            ])
        )
    )

def main(page: ft.Page):
    page.title = "VeteransHUB"
    page.theme_mode = "light"
    page.bgcolor = "#F8F6F0"
    
    # Контейнер для динамічного контенту
    main_content = ft.Container(expand=True)

    def catalog_view():
        businesses = get_businesses_from_sheet()
        if not businesses:
            return ft.Text("Дані не знайдено або помилка підключення.", color="red")
        
        cards = [create_business_card(b.get("Назва", "Бізнес"), b.get("Категорія", "-"), b.get("Опис", "")) for b in businesses]
        return ft.Column([ft.Text("Каталог", size=24), *cards])

    def navigate_to(e):
        if e.control.data == "catalog":
            main_content.content = catalog_view()
        else:
            main_content.content = ft.Text("Головна сторінка")
        page.update()

    # Appbar та Drawer спрощено для веб-сумісності
    page.appbar = ft.AppBar(title=ft.Text("VETERANS HUB"))
    page.add(main_content)

# Запуск програми
if __name__ == "__main__":
    ft.app(target=main)
