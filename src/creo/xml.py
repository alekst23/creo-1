import re
from pydantic import BaseModel
from typing import Optional
from typing import List

class XMLNode():
    tag: str
    attributes: Optional[dict]
    children: Optional[list]
    text: Optional[str]

    def __init__(self, tag, attributes={}, children=[], text=""):
        self.tag = tag
        self.attributes = attributes
        self.children = children
        self.text = text


class XMLParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(xml)->List[XMLNode]:
        # Use regex to find all matching opening and closing tags
        tag_pattern = r'<(?P<tag>[\w-]+)(?P<attributes>[^>]*)>(?P<content>.*?)</\1>'
        matches = re.finditer(tag_pattern, xml, re.DOTALL)

        nodes = []
        for match in matches:
            tag = match.group('tag')
            attributes = XMLParser._parse_attributes(match.group('attributes'))
            content = match.group('content').strip()
            children = XMLParser._parse_children(content)
            node = XMLNode(tag=tag, attributes=attributes, children=children, text=content)
            nodes.append(node)

        return nodes

    @staticmethod
    def _parse_attributes(attributes_str):
        # Use regex to parse attributes from a string
        attr_pattern = r'(\w+)="([^"]*)"'
        attributes = dict(re.findall(attr_pattern, attributes_str))
        return attributes

    @staticmethod
    def _parse_children(content):
        # Recursively parse children nodes
        return XMLParser.parse(content) if content else []


