""" Zarządzanie listą artykułów ze strony deloitte
"""
# Standard library imports
import os.path
import sys

# Third party imports
import argparse
from bs4 import BeautifulSoup
import requests
import traceback
import xml.etree.ElementTree as ET

# Third party imports
import src.xml_support as xml_support


def get_page_content(url: str) -> str:
    """ Pobranie zawartość strony www

    Na podstawie podanego adresu url funkcja pobiera i zwraca zawartość strony internetowej.

    :param url: Pełny adres strony internetowej
    :type url: str
    :return: HTML z zawartością strony spod podanego adresu url.
    :rtype: str
    """
    try:
        response = requests.get(url)
        if not response.ok:
            response.raise_for_status()
        else:
            return response.text
    except requests.exceptions.RequestException as err:
        print(err.__class__, err)
        return ''


def get_articles(html: str) -> list:
    """ Pobranie informacji o artykułach.

    Funkcja wyszukuje w otrzymanym html-u artykuły i zwraca informacje o nich. Każdy artykuł zawiera tytuł oraz link do
    strony www

    :param html: Html, w którym zawarte są artykuły
    :type html: str
    :return: Lista z informacjami o artykułach
    :rtype: list[[tytuł,link], [tytuł,link]]
    :exception: W przypadku, gdy w podanym html-u nie było artykułów to generowany jest wyjątek
    """

    list_articles = []
    soup = BeautifulSoup(html, features="lxml")

    for tag in soup.find_all('h2'):
        parent = tag.find_parent('a')
        link = parent.get('href')
        list_articles.append([remove_characters(tag.text), link])

    for tag in soup.find_all(class_='standard-promo perspective-color'):
        parent = tag.find_parent('a')
        link = parent.get('href')
        list_articles.append([remove_characters(tag.h3.text), link])

    if len(list_articles) == 0:
        raise Exception("ERROR: I did not find the articles")

    return list_articles


def remove_characters(string: str) -> str:
    """ Usuwanie zbędnych znaków z tekstu

    Funkcja usuwa znak u'\xa0' (No-Break Space - &nbsp) oraz białe znaki z podanego ciągu znaków.

    :param string: Ciąg znaków, z którego usuwane są znaki
    :type string: str
    :return: Ciąg znaków po usunięciu wskazanych znaków
    :rtype: str
    """
    string = string.strip()
    return string.replace(u'\xa0', ' ')


def complete_link(link):
    """ Uzupełnienie linku do artykułu.

    Funkcja kompletuje podany link względny do artykułu. Dodaje do niego przedrostek z adresem strony
    'https://www2.deloitte.com/'.

    :param link: Względny link do artykułu
    :type link: str
    :return: Pełny link do artykułu
    :rtype: str
    """
    return "https://www2.deloitte.com/" + link


# TODO: dodać testy jednostkowe
def xml_create_article(title, link, is_new) -> ET.Element:
    """ Utworzenie xml-a z informacjami o artykule.

    Funkcja na podstawie otrzymanych parametrów generuje obiekt xml z informacjami o artykule.

    :return:
    :param title: Tytuł artykułu
    :type title: str
    :param link: Link do artykułu
    :type link: str
    :param is_new: True - jeżeli jest to nowy artykuł. False - jeżeli artykuł jest już zapisany w źródle danych
    :type is_new: bool
    :return: Obiekt xml z informacjami o artykule
    :rtype: xml.etree.ElementTree.Element
    """
    node_article = ET.Element('article')
    node_article.set('new', str(is_new).lower())
    node_article.set('read', str(False).lower())

    node_title = ET.SubElement(node_article, 'title')
    node_title.text = title

    node_link = ET.SubElement(node_article, 'link')
    node_link.text = complete_link(link)

    return node_article


# TODO: dodać testy jednostkowe
def xml_load_tree(file_name: str) -> ET.ElementTree:
    """ Załadowanie xml-a z danymi o artykułach

    Funkcja ładuje dane o artykułach z podanego pliku xml. Jeżeli plik nie istnieje to funkcja tworzy nowy plik z
    podstawowymi informacjami xml oraz węzłem root.

    :param file_name: Nazwa pliku xml z danymi o artykułach
    :type file_name: str
    :return: Obiekt xml z zawartością podanego pliku xml.
    :rtype: xml.etree.ElementTree.Element
    """
    if not os.path.exists(file_name):
        xml_create_tree(file_name)
    return ET.parse(file_name)


# TODO: dodać testy jednostkowe
def xml_create_tree(file_name):
    """ Utworzenie głównego węzła xml

    Funkcja tworzy główny węzeł w pliku xml i zapisuje utworzony xml do podanego pliku.

    :param file_name: Nazwa pliku xml
    :type file_name: str
    :return: ---
    :rtype: ---
    """
    doc = ET.Element('articles')
    tree = ET.ElementTree(doc)
    xml_support.xml_save_to_file(tree, file_name)


# TODO: dodać testy jednostkowe
def xml_modify_tree(articles_list, root_node: ET.Element) -> int:
    """ Modyfikacja zawartości xml-a z informacjami o artykułach

    Funkcja otrzymuje listę artykułów odczytaną ze strony www oraz xml z artykułami zapisany na dysku. Następnie
    porównuje zawartość obu źródeł i dodaje do xml-a artykuły odczytane ze strony www, których nie ma w xml-u.
    Funkcja modyfikuje zawartość podanego xml-a.

    :param articles_list: Lista artykułów odczytana ze strony www w postaci list[[tytuł,link], [tytuł,link]]
    :type articles_list: list[[str,str], [str,str]]
    :param root_node: Obiekt xml z danymi o artykułach, które zapisane są w pliku xml
    :type root_node: xml.etree.ElementTree.Element
    :return: Ilość nowo dodanych artykułów
    :rtype: int
    """
    new_articles_count = 0
    for article in articles_list:
        article_already_exists = False
        for node in root_node.iter(tag='title'):
            if node is not None:
                if node.text == article[0]:
                    article_already_exists = True
                    break
        if not article_already_exists:
            new_article_node = xml_create_article(title=article[0], link=article[1], is_new=True)
            root_node.append(new_article_node)
            new_articles_count += 1
    return new_articles_count


# TODO: Dodać testy jednostkowe
def get_command_arguments() -> tuple:
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', help='Show information about script', action='store_true', default=False)
    parser.add_argument('-i', '--info', action='store_true', help="Show information about articles", default=False)
    args = parser.parse_args()
    return args.version, args.info


# TODO: Dodać testy jednostkowe
def show_articles_info():
    xml_tree_local = xml_load_tree(xml_file_path)
    amount_all, amount_new, amount_read = find_all_articles(xml_tree_local.getroot())
    print(f"All articles: {amount_all}\nNew articles: {amount_new}\nReaded articles: {amount_read}")


# TODO: Dodać testy jednostkowe
def find_all_articles(xml_root: ET.ElementTree):
    amount, new, read = 0, 0, 0
    for node in xml_root.findall("article"):
        amount += 1
        if node.get('new').lower() == 'true':
            new += 1
        if node.get("read").lower() == 'true':
            read += 1
    return amount, new, read


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Konfiguracja
    xml_file_path = os.path.join('savedArticles', 'artcs.xml')
    print(os.getcwd())

    # Parser parametrów linii komend
    version, info = get_command_arguments()
    if version:
        print("This is version 1.0 written by PiotrZET")
        exit(0)
    if info:
        show_articles_info()
        exit(0)

    try:
        # - Czytamy artykuły ze strony i budujemy listę odczytanych artykułów (tytuł oraz link)
        # - odczytujemy plik xml z artykułami
        #   - jeżeli pliku nie ma to go tworzymy na nowo
        # - przechodzimy przez listę artykułów ze strony
        #   - sprawdzamy czy artykuł jest w pliku
        #       - jak jest to go pomijamy, a jak nie ma to dodajemy do pliku z atrybutem NEW
        # - zapisujemy zmieniony plik

        # print(get_articles.__doc__)
        # help(get_articles)
        content = get_page_content(url='https://www.deloitte.com/pl/pl/pages/technology/topics/blog-agile.html')
        if content:
            articles = get_articles(html=content)
            xml_tree = xml_load_tree(xml_file_path)
            added_articles = xml_modify_tree(articles, xml_tree.getroot())
            xml_support.xml_save_to_file(xml_tree, xml_file_path)
            print(f"Dodano {added_articles} nowych artykułów.\nDziałanie programu zakończone.")
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('*' * 100, 'print_tb')
        traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)

        print('*' * 100, 'print_exception:')
        # exc_type below is ignored on 3.5 and later
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)

        print('*' * 100, 'print_exc:')
        traceback.print_exc(limit=2, file=sys.stdout)

        print('*' * 100, 'format_exc, first and last line:')
        formatted_lines = traceback.format_exc().splitlines()
        # print(formatted_lines[0])
        # print(formatted_lines[-1])

        print('*' * 100, 'format_exception:')
        # exc_type below is ignored on 3.5 and later
        print(repr(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback)))

        print('*' * 100, 'extract_tb:')
        print(repr(traceback.extract_tb(exc_traceback)))

        print('*' * 100, 'format_tb:')
        print(repr(traceback.format_tb(exc_traceback)))

        print('*' * 100, 'tb_lineno:', exc_traceback.tb_lineno)
        exit()
