from secrets import token_hex
from typing import Dict, List
from xml.dom.minidom import Element

from fgui.Decoder import ADecoder
from fgui.utils import to_hex


class Group(ADecoder):
    def __init__(self, data: Dict, node: Element):
        super().__init__(data, node)

    def decode(self, out_assets: List[tuple[tuple[str, str],...]]):
        self._add_basic_attrs()
