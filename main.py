import flet as ft

def main(page: ft.Page):
    page.title = "VeteransHUB" 
    page.window.width = 390
    page.window.height = 844
    page.theme_mode = "light"
    page.bgcolor = "#F8F6F0" 
    page.padding = 0
    page.scroll = "auto" 

    # --- 🧭 ЛОГІКА НАВІГАЦІЇ ---
    main_content = ft.Container(expand=True) 

    def navigate_to(view_name):
        page.drawer.open = False
        main_content.content = get_view(view_name)
        page.update()

    def show_menu(e):
        page.drawer.open = True
        page.update()

    # --- 🧠 ФУНКЦІЯ ВИБОРУ ЕКРАНУ ---
    def get_view(name):
        if name == "catalog":
            return catalog_view()
        else:
            return home_view()

    # --- 🍔 БОКОВЕ МЕНЮ ---
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

    # --- 🎩 ВЕРХНЯ ПАНЕЛЬ ---
    page.appbar = ft.AppBar(
        # ВИПРАВЛЕНО: Замість IconButton використовуємо Container з текстом-іконкою
        leading=ft.Container(
            content=ft.Text("☰", size=24, color="black"), 
            padding=15, 
            ink=True, 
            on_click=show_menu
        ),
        title=ft.Row([ft.Text("VETERANS", size=26, font_family="Impact"), ft.Text("HUB", weight="bold", size=32, color="#8B0000", italic=True)], alignment="center"),
        center_title=True, bgcolor="#F8F6F0"
    )

    # --- 🏠 ГОЛОВНИЙ ЕКРАН ---
    def home_view():
        return ft.Column([
            ft.Container(height=10),
            build_catalog_section(), 
            ft.Container(height=20)
        ])

    # --- 🛍️ ЕКРАН КАТАЛОГУ ---
    def catalog_view():
        return ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Повний каталог", size=24, weight="bold"),
                ft.Text("Тут будуть всі бізнеси..."),
                ft.ElevatedButton("Назад на головну", on_click=lambda e: navigate_to("home"))
            ])
        )

    # --- 📄 ЕЛЕМЕНТИ (НЕЗМІННІ) ---
    def cat_icon(url, text):
        return ft.Container(
            content=ft.Column([
                ft.Image(src=url, width=28, height=28, color="black"),
                ft.Text(text, size=10, weight="w_700", color="black", text_align="center", max_lines=1) 
            ], horizontal_alignment="center", spacing=4),
            bgcolor="#EBE9E2", width=88, height=85, border_radius=15, padding=5, ink=True,
            on_click=lambda e: navigate_to("catalog"), data=text
        )

    def build_catalog_section():
        categories_grid = ft.Column([
            ft.Row([cat_icon("https://img.icons8.com/ios-filled/50/coffee.png", "Кафе"), cat_icon("https://img.icons8.com/ios-filled/50/shop.png", "Магазин"), cat_icon("https://img.icons8.com/ios-filled/50/maintenance.png", "Послуги")], alignment="spaceBetween"),
            ft.Row([cat_icon("https://img.icons8.com/ios-filled/50/macbook.png", "Техніка"), cat_icon("https://img.icons8.com/ios-filled/50/truck.png", "Логістика"), cat_icon("https://img.icons8.com/ios-filled/50/settings.png", "Виробництво")], alignment="spaceBetween"),
            ft.Row([cat_icon("https://img.icons8.com/ios-filled/50/scales.png", "Юристи"), cat_icon("https://img.icons8.com/ios-filled/50/psychology.png", "Психологи"), cat_icon("https://img.icons8.com/ios-filled/50/box.png", "Доставка")], alignment="spaceBetween"),
        ], spacing=10)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("КАТАЛОГ VETERANSBIZ", weight="heavy", size=14, color="#374151"),
                categories_grid,
                ft.Container(height=10),
                ft.Container(
                    content=ft.Text("Перейти до каталогу", weight="bold", size=16, color="black"),
                    bgcolor="#EBE9E2", padding=15, border_radius=15, alignment="center",
                    on_click=lambda e: navigate_to("catalog"), ink=True
                )
            ], spacing=15),
            bgcolor="white", padding=20, border_radius=25, margin=20
        )

    # Ініціалізація
    main_content.content = home_view()
    page.add(main_content)

if __name__ == "__main__":
    ft.run(main)
