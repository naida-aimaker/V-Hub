import flet as ft
import os
import json
import gspread
from dotenv import load_dotenv

# --- 🔐 НАЛАШТУВАННЯ БЕЗПЕКИ ---
load_dotenv() 

def get_google_sheets():
    try:
        creds_json_string = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if not creds_json_string:
            return None
        creds_dict = json.loads(creds_json_string)
        gc = gspread.service_account_from_dict(creds_dict)
        return gc
    except Exception as e:
        print(f"Помилка підключення до Google Sheets: {e}")
        return None

gc = get_google_sheets()

# --- 📊 РОБОТА З ДАНИМИ ---
def get_businesses_from_sheet():
    if not gc:
        return []
    try:
        sh = gc.open("V-Hub_Database")
        # Тепер ми точно звертаємося до аркуша "Businesses"
        worksheet = sh.worksheet("Businesses") 
        return worksheet.get_all_records()
    except Exception as e:
        print(f"Помилка завантаження даних: {e}")
        return []

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

# --- 🏠 ОСНОВНИЙ ІНТЕРФЕЙС ---
def main(page: ft.Page):
    page.title = "VeteransHUB" 
    page.window.width = 390
    page.window.height = 844
    page.theme_mode = "light"
    page.bgcolor = "#F8F6F0" 
    page.padding = 0
    page.scroll = "auto" 

    main_content = ft.Container(expand=True) 

    def navigate_to(view_name):
        page.drawer.open = False
        main_content.content = get_view(view_name)
        page.update()

    def show_menu(e):
        page.drawer.open = True
        page.update()

    def get_view(name):
        if name == "catalog":
            return catalog_view()
        else:
            return home_view()

    # --- 🍔 МЕНЮ ---
    def menu_item(emoji, title, data=""):
        return ft.Container(
            content=ft.Row([ft.Text(emoji, size=22), ft.Container(width=10), ft.Text(title, weight="bold", size=16)]),
            padding=10, ink=True, on_click=lambda e: navigate_to(data), data=data
        )

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(padding=20, content=ft.Column([
                ft.Text("Меню", size=24, weight="heavy"),
                ft.Divider(),
                menu_item("📍", "Карта", "home"),
                menu_item("🏪", "Каталог", "catalog"),
                menu_item("🚪", "Головна", "home"),
            ]))
        ]
    )

    page.appbar = ft.AppBar(
        leading=ft.Container(content=ft.Text("☰", size=24, color="black"), padding=15, ink=True, on_click=show_menu),
        title=ft.Row([ft.Text("VETERANS", size=26, font_family="Impact"), ft.Text("HUB", weight="bold", size=32, color="#8B0000", italic=True)], alignment="center"),
        center_title=True, bgcolor="#F8F6F0"
    )

    # --- 🏠 ГОЛОВНИЙ ЕКРАН ---
    def home_view():
        return ft.Column([ft.Container(height=10), build_catalog_section(), ft.Container(height=20)])

    # --- 🛍️ КАТАЛОГ ---
    def catalog_view():
        try:
            businesses = get_businesses_from_sheet()
            if not businesses:
                return ft.Container(padding=20, content=ft.Column([
                    ft.Text("Помилка або таблиця порожня!", size=20, color="red"),
                    ft.ElevatedButton("Назад", on_click=lambda e: navigate_to("home"))
                ]))
            
            cards = [create_business_card(b.get("Назва", "Бізнес"), b.get("Категорія", "-"), b.get("Опис", "")) for b in businesses]
        except Exception as e:
            return ft.Container(padding=20, content=ft.Text(f"Критична помилка: {str(e)}"))
        
        return ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Повний каталог", size=24, weight="bold"),
                *cards,
                ft.ElevatedButton("Назад на головну", on_click=lambda e: navigate_to("home"))
            ])
        )

    def build_catalog_section():
        return ft.Container(content=ft.Text("Натисніть нижче, щоб побачити каталог"), bgcolor="white", padding=20) 

    main_content.content = home_view()
    page.add(main_content)

if __name__ == "__main__":
    ft.run(main)
