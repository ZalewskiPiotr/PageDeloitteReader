import xml.etree.ElementTree as ET


# TODO: dodać testy jednostkowe
def xml_save_to_file(tree: ET.ElementTree, filename):
    """ Zapis do pliku xml-a z informacjami o artykułach.

    Funkcja zapisuje do pliku pod podaną nazwą zawartość xml-a z danymi o artykułach

    :param tree: Obiekt xml z danymi o artykułach
    :type tree: xml.etree.ElementTree.ElementTree
    :param filename: Nazwa pliku xml
    :type filename: str
    :return: ---
    :rtype: ---
    """
    tree.write(file_or_filename=filename, xml_declaration=True, encoding='utf-8', method='xml',
               short_empty_elements=False)