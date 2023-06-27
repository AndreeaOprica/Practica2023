import random
from datetime import datetime
from dateutil.parser import parse as parse_date
from playwright.sync_api import sync_playwright
import pandas as pd
from urllib.parse import urlencode


def validate_date(date_string):
    try:
        date = parse_date(date_string)
        if date.date() < datetime.now().date():
            print("Data introdusă este mai veche decât data curentă.")
            return False
        return True
    except ValueError:
        print("Formatul datei este incorect.")
        return False


def validate_positive_integer(value):
    try:
        int_value = int(value)
        if int_value < 0:
            raise ValueError
        return True
    except ValueError:
        return False


def get_valid_input(prompt, validate_func):
    while True:
        user_input = input(prompt)
        if validate_func(user_input):
            return user_input
        else:
            print("Valoarea introdusă este invalidă. Vă rugăm reintroduceți.")


def main():
    max_attempts = 3
    attempts = 0

    checkin_date = None
    checkout_date = None
    destinatie = None
    adults = None
    children = None
    rooms = None
    pet_friendly = False

    while attempts < max_attempts:
        if not checkin_date:
            checkin_date = get_valid_input("Introduceti data de check-in (YYYY-MM-DD): ", validate_date)

        if not checkout_date:
            checkout_date = get_valid_input("Introduceti data de check-out (YYYY-MM-DD): ", validate_date)

        if parse_date(checkout_date) < parse_date(checkin_date):
            print("Data de check-out nu poate fi mai devreme decât data de check-in.")
            checkout_date = None
            continue

        if not destinatie:
            destinatie = input("Introduceti destinatia: ")
            if not destinatie:
                print("Destinatia nu poate fi goala.")
                continue

        if adults is None:
            adults = get_valid_input("Introduceti numarul de adulti: ", validate_positive_integer)
            adults = int(adults)

        if children is None:
            children = get_valid_input("Introduceti numarul de copii (0 sau mai mare): ", validate_positive_integer)
            children = int(children)

        if rooms is None:
            rooms = get_valid_input("Introduceti numarul de camere: ", validate_positive_integer)
            rooms = int(rooms)

        if attempts >= max_attempts:
            print("Ati depasit numarul maxim de incercari. Programul se inchide.")
            return

        pet_friendly_input = input("Este necesară opțiunea de pet-friendly? (da/nu): ").lower()
        if pet_friendly_input in ["da", "nu"]:
            pet_friendly = pet_friendly_input == "da"
            break
        else:
            print("Opțiunea pet-friendly poate fi doar 'da' sau 'nu'.")
            continue

    query_params = {
        "checkin": checkin_date,
        "checkout": checkout_date,
        "selected_currency": "USD",
        "ss": destinatie,
        "ssne": destinatie,
        "ssne_untouched": destinatie,
        "lang": "en-us",
        "sb": "1",
        "src_elem": "sb",
        "src": "searchresults",
        "dest_type": "city",
        "group_adults": adults,
        "no_rooms": rooms,
        "group_children": children,
        "sb_travel_purpose": "leisure",
        "nflt": "1" if pet_friendly else "0"
    }

    query_string = urlencode(query_params)
    page_url = f'https://www.booking.com/searchresults.en-us.html?{query_string}'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels.')

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            price_element = hotel.locator('//span[@data-testid="price-and-discounted-price"]')
            hotel_dict['price'] = price_element.inner_text() if price_element.is_visible() else ""
            score_element = hotel.locator('//div[@data-testid="review-score"]/div[1]')
            hotel_dict['score'] = score_element.inner_text() if score_element.is_visible() else ""
            avg_review_element = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]')
            hotel_dict['avg review'] = avg_review_element.inner_text() if avg_review_element.is_visible() else ""
            reviews_count_element = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]')
            hotel_dict['reviews count'] = reviews_count_element.inner_text().split()[0] if reviews_count_element.is_visible() else ""

            hotels_list.append(hotel_dict)

        df = pd.DataFrame(hotels_list)
        # df_sorted = df.sort_values(by='score', ascending=False)
        df_sorted = df.sort_values(by='score', key=lambda x: pd.to_numeric(x, errors='coerce'), ascending=False)

        random_number = random.randint(0, 99)
        
        csv_filename = f'{destinatie}_{random_number}_hotels_list.csv'
        excel_filename = f'{destinatie}_{random_number}_hotels_list.xlsx'
        
        df_sorted.to_csv(csv_filename, index=False)
        print(f"CSV-ul a fost salvat cu succes în fișierul '{csv_filename}'.")

        df_sorted.to_excel(excel_filename, index=False)
        print(f"Excelul a fost salvat cu succes în fișierul '{excel_filename}'.")

        browser.close()


if __name__ == '__main__':
    main()
