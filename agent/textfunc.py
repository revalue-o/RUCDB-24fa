import xml.etree.ElementTree as ET


def text2func(text):
    text = text.replace("\n", "")
    text = text.replace(" ", "")

    start_tag = '<funccall>'
    end_tag = '</funccall>'
    xml_start_index = text.find(start_tag)
    xml_end_index = text.find(end_tag) + len(end_tag)

    if xml_start_index != -1 and xml_end_index != -1:
        text = text[xml_start_index:xml_end_index]
    else:
        return None, None, None

    root = ET.fromstring(text)
    function = root.find('function').text
    parameter = root.find('parameter').text

    return  function, parameter