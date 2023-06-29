# Practica2023

                                                   Booking.com Hotel Search

     Acest proiect este un script Python pentru căutarea și afișarea hotelurilor pe Booking.com în funcție de anumite criterii.

      Funcționalități:

- Solicită utilizatorului să introducă datele necesare pentru căutarea hotelurilor, cum ar fi data de check-in, data de check-out, destinația, numărul de adulți și copii, numărul de camere și opțiunea pet-friendly;
- Validează datele introduse de utilizator pentru a se asigura că sunt în formatul corect și că respectă anumite reguli, cum ar fi data de check-out să nu fie mai devreme decât data de check-in;
- Salvează datele de utilizator într-un fișier CSV pentru a le putea accesa ulterior;
- Utilizează librăria Playwright pentru a accesa pagina Booking.com și a căuta hoteluri în funcție de criteriile introduse de utilizator;
- Extrage informații relevante despre hoteluri, cum ar fi numele, prețul, scorul de evaluare și numărul de recenzii;
- Afișează numărul total de hoteluri găsite și salvează rezultatele într-un fișier CSV și un fișier Excel pentru a le putea vizualiza mai târziu;
- Generează o diagramă vizuală utilizând biblioteca Matplotlib pentru a reprezenta scorurile de evaluare ale hotelurilor sub formă de bare orizontale;
- Oferă opțiunea de a afișa datele de utilizator introduse anterior, pentru a le putea consulta rapid.


     Structura de fișiere:

- `script.py`: Scriptul principal Python;
- `user_data.csv`: Fișierul CSV pentru stocarea datelor de utilizator introduse anterior;
- `README.md`: Acest fișier, care conține informații detaliate despre proiect.



