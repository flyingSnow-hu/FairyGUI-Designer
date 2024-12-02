from abc import ABCMeta, abstractmethod
from typing import Dict, List
from xml.dom.minidom import Document, Element

from fgui.utils import get_id_hash, get_part_before_colon


class ADecoder(metaclass=ABCMeta):
    def __init__(self, data:Dict, node:Element):
        self.data = data
        self.node = node
        self.offset_x = 0
        self.offset_y = 0

    @property
    def id(self):
        return get_id_hash(self.data['id'])

    def set_group_id(self, group_id:str):
        self.node.setAttribute('group', group_id)


    @abstractmethod
    def decode(self, out_assets: List[tuple[tuple[str, str],...]]):
        # node = doc.createElement('text')
        pass

    # @abstractmethod
    def add_to_package(self, package_doc:Document) -> Element|None:
        return None
    
    # def add_self_to_package(self, package_doc:Document) -> Element:


    def _add_basic_attrs(self):
        # text_element = doc.createElement('text')
        self.node.setAttribute('id', self.id)
        self.node.setAttribute('name', get_part_before_colon(self.data['name']))
        self.node.setAttribute('xy',
                                  f"{self.data['absoluteBoundingBox']['x'] + self.offset_x:.0f},{self.data['absoluteBoundingBox']['y'] + self.offset_y:.0f}")
        self.node.setAttribute('size',
                                  f"{self.data['absoluteBoundingBox']['width']:.0f},{self.data['absoluteBoundingBox']['height']:.0f}")
        # self.node.setAttribute('fontSize', str(self.data['style']['fontSize']))
        # self.node.setAttribute('text', self.data['characters'])
        # display_list.appendChild(text_element)

    def set_attr(self, name, value):
        self.node.setAttribute(name, str(value))

    def set_offset(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y