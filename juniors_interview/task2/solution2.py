import requests
from bs4 import BeautifulSoup
import csv

# URL категории животных
URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"

def fetch_animal_counts():
    letter_counts = {}
    next_page = URL

    while next_page:
        # Загружаю HTML-страницу, прежде убедившись, что код запроса был 200
        response = requests.get(next_page)
        if response.status_code != 200:
            print(f"Ошибка при загрузке страницы: {response.status_code}")
            break

        # Парсим страницу
        soup = BeautifulSoup(response.text, "html.parser")

        # Извлекаем список животных
        items = soup.select(".mw-category-group ul li a")
        for item in items:
            name = item.text
            if name:  # Проверяем, что текст не пустой
                first_letter = name[0].upper()
                if "А" <= first_letter <= "Я":  # Проверяем, что это буква русского алфавита (Так как про другие ничего не было сказано)
                    letter_counts[first_letter] = letter_counts.get(first_letter, 0) + 1

        # Находим ссылку на следующую страницу
        next_link = soup.find("a", string="Следующая страница")
        next_page = f"https://ru.wikipedia.org{next_link['href']}" if next_link else None

    return letter_counts

def save_to_csv(data, filename="beasts.csv"):
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        for letter, count in sorted(data.items()):
            writer.writerow([letter, count])

def main():
    print("Собираем данные о животных...")
    animal_counts = fetch_animal_counts()
    print("Сохранение результатов в файл...")
    save_to_csv(animal_counts)
    print(f"Данные успешно сохранены в 'beasts.csv'., чекайте")

if __name__ == "__main__":
    main()
