import src.deloitte as deloitte
import pytest

url_string = [("https1://www2.deloitte.com/pl/pl/pages/technology/topics/blog-agile.html", ""),
              ("https://www8.deloitte.com/pl/pl/pages/technology/topics/blog-agile.html", ""),
              ("https://www2.deloitte.com/pl/pl/pages/technology/topics/blog-agile.html1", ""),
              ("", "")]


# TODO: W teście jest odwołanie do adresu URL. Na coś to zamienić bo nie jest to test jednostkowy
def test_get_page_content():
    """ Sprawdzenie czy funkcja zwraca jakąś zawartość - cokolwiek """
    # given
    url = "https://www2.deloitte.com/pl/pl/pages/technology/topics/blog-agile.html"
    # when
    result = deloitte.get_page_content(url).split()
    # then
    assert len(result) > 0


@pytest.mark.parametrize("url, result", url_string)
def test_get_page_content_request_error(url, result):
    """ Sprawdzenie czy funkcja zwróci błąd po podaniu nieprawidłowego adresu url """
    # given
    # when
    result = deloitte.get_page_content(url)
    # then
    assert not result


# TODO: dane do testu nie mogą być pobierane z pliku. Trzeba to jakoś w kodzie zakodować
def test_get_articles():
    """ Sprawdzenie czy funkcja zwraca prawidłową liczbę artykułów. W danych wzorcowych jest ich 59. """

    # given
    with open('test_data_get_articles.txt', 'r') as data_file:
        html = data_file.read()
    with open('test_resultdata_get_articles.txt', 'r') as result_data_file:
        expected_value = list(result_data_file.read().split(';'))
    # when
    result = deloitte.get_articles(html)
    # then
    expected_length = len(expected_value)
    length = len(result)
    assert length == expected_length


def test_get_articles1():
    """ Sprawdzenie czy pojawia się wyjątek przy podaniu pustego HTML-a do funkcji"""
    html = ''
    with pytest.raises(Exception):
        result = deloitte.get_articles(html)


def test_complete_link():
    """ Sprawdzenie czy funkcja prawidłowo skleja link z podanych ciągów. """
    # given
    prefix = "https://www2.deloitte.com/"
    link = "/page/pl-pl/index.html"
    # when
    complete_link = deloitte.complete_link(link)
    # then
    assert prefix + link == complete_link


def test_get_articles_verify_type():
    """ Sprawdzenie czy obiekt listy jest kolejną listą """

    # given
    with open('test_data_get_articles.txt', 'r') as data_file:
        html = data_file.read()
    # when
    list_articles = deloitte.get_articles(html)
    # then
    assert type(list_articles[0]) is list


def test_remove_characters():
    """ Sprawdzenie czy zostały usunięte znaki specjalne oraz białe znaki z podanego stringu """
    # given
    src_string = "Something \xa0 is in our garden "
    # when
    result_string = deloitte.remove_characters(src_string)
    # then
    assert result_string.find("\xa0") == -1
    assert len(result_string) == len(result_string.strip())


@pytest.mark.skip(reason="Zapis do pliku nie jest testem jednostkowym. Tu chyba jakiś mock jest potrzebny")
def test_save_to_file():
    pass