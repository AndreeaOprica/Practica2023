from playwright.sync_api import sync_playwright
import pandas as pd
import random
import datetime
import os


def main():

    checkin_date = input("Introduceti data de check-in (YYYY-MM-DD): ")
    checkout_date = input("Introduceti data de check-out (YYYY-MM-DD): ")
    destinatie = input("Introduceti destinatia: ")
    num_adulti = int(input("Introduceti numarul de adulti: "))
    num_copii = int(input("Introduceti numarul de copii: "))
    pet_friendly = input("Doriti hotel pet-friendly? (da/nu): ")

    try_count = 0
    while try_count < 3:
        try:

            datetime.datetime.strptime(checkin_date, "%Y-%m-%d")
            datetime.datetime.strptime(checkout_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Data introdusa nu este in formatul corect (YYYY-MM-DD)!")
            try_count += 1
            if try_count == 3:
                print("Ati introdus de 3 ori datele in format incorect. Programul se inchide.")
                return
            checkin_date = input("Introduceti data de check-in (YYYY-MM-DD): ")
            checkout_date = input("Introduceti data de check-out (YYYY-MM-DD): ")

    try:

        current_date = datetime.datetime.now().date()
        if datetime.datetime.strptime(checkin_date, "%Y-%m-%d").date() < current_date:
            raise ValueError("Data de check-in nu poate fi anterioară datei curente!")


        random_num = str(random.randint(100, 999))


        page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=USD&ss={destinatie}&ssne={destinatie}&ssne_untouched={destinatie}&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults={num_adulti}&no_rooms=1&group_children={num_copii}&sb_travel_purpose=leisure'

        if pet_friendly.lower() == "da":
            page_url += "&nflt=pets-1"

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
                hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
                hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
                hotel_dict['avg review'] = hotel.locator(
                    '//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
                hotel_dict['reviews count'] = \
                    hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

                hotels_list.append(hotel_dict)

            df = pd.DataFrame(hotels_list)


            df['score'] = df['score'].astype(float)
            df.sort_values(by='score', ascending=False, inplace=True)


            csv_path = f"{destinatie}_{random_num}_hotels_list.csv"
            excel_path = f"{destinatie}_{random_num}_hotels_list.xlsx"

            df.to_csv(csv_path, index=False)
            df.to_excel(excel_path, index=False)

            print(f"Fisierele CSV si Excel au fost create: {csv_path}, {excel_path}")

            browser.close()

    except ValueError as e:
        print(str(e))
        return


if __name__ == '__main__':
    main()