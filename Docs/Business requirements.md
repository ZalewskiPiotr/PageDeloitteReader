# WERSJA 5.0 - planowana
- jeżeli pojawiły się nowe artykuły to wyślij informację o nich na maila

# WERSJA 4.0 - planowana
- dodać możliwość wyświetlenia tylko nowych artykułów (cmd --show new)
- dodać możliwość wyświetlenia tylko przeczytanych artykułów (cmd --show read)
- dodać możliwość wyświetlenia wszystkich artykułów (cmd --show all)
- przerobić na program obiektowy
- utworzyć odpowiednią strukturę katalogów dla projektu. 
- Dodać jakiś plik ini z informacją o wersji, autorze, itd

# WERSJA 3.0 - w trakcie
- obsługa błędów - w przypadku, gdy wystąpi wyjątek to wyświetlać użytkownikowi ładny komunikat, a stos wyjątku zapisać w pliku w katalogu './logs'
  - obsłużyć zdarzenia: odczyt nieprawidłowego xml-a, błąd przy zapisie xml-a
- (OK) przenieść zapis pliku xml z artykułami do katalogu './articles'
- dodać możliwość zmiany w pliku xml parametru 'read'
- dodać możliwość zmiany w pliku xml parametru 'new'
- (OK) po załadowaniu artykułów wyświetlić informację ile nowych artykułów zostało dodanych
- dodać możliwość konfiguracji programu (numer wersji, autor, data wydania, konfiguracja katalogów zapisu danych)
- Dodać możliwość wyświetlenia konfiguracji poprzez podanie parametru w linii poleceń
- (OK) Dodać możliwość wyświetlenia informacji
  - (OK) ile artykułów jest w pliku
  - (OK) ile artykułów jest oznaczonych jako NEW
  - (OK) ile artykułów jest oznaczonych jako przeczytanych
- dodać dokumentację do nowych funkcji
- dodać testy jednostkowe do nowych funkcji

# WERSJA 2.0 - w trakcie
- (OK) artykuły należy przechowywać w jednym pliku xml lub json. 
  - (OK) jeżeli pliku nie ma, to należy go utworzyć 
  - (OK) do pliku należy dodawać artykuły, które są na stronie a nie ma ich w pliku. Każdy taki artykuł musi dostać znacznik NEW 
- (OK) należy rozbudować informacje o artykule o link do artykułu, tak aby gdzieś przy nazwie był łatwy do kliknięcia link
- (OK) każda pozycja w pliku musi mieć miejsce na wstawienie znacznika, że artykuł został przeczytany
- (OK) zbudować i wygenerować dokumentację deweloperską
- test jednostkowy dla get_page_content - zrobić mocka na pobieranie danych ze strony www, tak aby zrezygnować z odwołania się do adresu url na zewnętrznym serwerze 
- test jednostkowy dla save_to_file - może też jako mock a może jako fixture tmpdir (czy coś podobnego)
- (OK) test jednostkowy test_get_articles_verify_dimension

# WERSJA 1.0 0 - zakończona
- (OK) odczyt artykułów z podanego adresu
    - (OK) zaczynamy od adresu: https://www2.deloitte.com/pl/pl/pages/technology/topics/blog-agile.html
- (OK) zapis wszystkich artykułów do pliku txt
- (OK) testy jednostkowe dla programu
- (OK) dodać moduł do weryfikacji pokrycia kodu testami (pytest --cov-report html --cov=main test_main.py)