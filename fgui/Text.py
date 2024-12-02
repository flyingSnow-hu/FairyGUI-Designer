from typing import Dict, List
from xml.dom.minidom import Element

from fgui.Decoder import ADecoder
from fgui.utils import to_hex


class Text(ADecoder):
    def __init__(self, data: Dict, node: Element):
        super().__init__(data, node)

    def decode(self, out_assets: List[tuple[tuple[str, str],...]]):
        self._add_basic_attrs()

        # fontSize
        font = self.data['style']
        self.set_attr('fontSize', font['fontSize'])

        # text
        text = self.data['characters']
        self.set_attr('text', text)

        # input
        if self.data['name'].endswith(':Input'):
            self.set_attr('input', 'true')
