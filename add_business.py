import gspread

print("🤖 Підключаюся до бази даних V-Hub...")

# 1. Авторизація за допомогою ключа
gc = gspread.service_account(filename='credentials.json')

# 2. Відкриваємо таблицю за назвою
sh = gc.open('V-Hub_Database')

# 3. Вибираємо вкладку
worksheet = sh.worksheet("Businesses")

# 4. Дані для запису
new_business_data = [
    1,
    "Кав'ярня 'Позиція'",
    "Олександр",
    "Громадське харчування",
    "Затишна кав'ярня від ветерана 93-ї ОМБр.",
    "Київ",
    "+380991112233"
]

# 5. Додаємо рядок
worksheet.append_row(new_business_data)

print("✅ Успіх! Бізнес додано до Google Таблиці.")
