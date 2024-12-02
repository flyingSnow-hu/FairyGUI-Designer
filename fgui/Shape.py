from secrets import token_hex
from typing import Dict, List
from xml.dom.minidom import Element

from fgui.Decoder import ADecoder
from fgui.utils import to_hex


class Shape(ADecoder):
    def __init__(self, data: Dict, node: Element):
        super().__init__(data, node)

    def decode(self, out_assets: List[tuple[tuple[str, str],...]]):
        self._add_basic_attrs()
        self.set_attr('type', 'rect')

        # stoke
        line_size =  self.data['strokeWeight'] if 'strokeWeight' in self.data else 1
        line_color = '#FF000000'
        if len(self.data['strokes']) > 0:
            stroke = self.data['strokes'][0]
            color = stroke['color']
            line_color = to_hex(color['r'], color['g'], color['b'], color['a'])

        self.set_attr('lineSize', line_size)
        self.set_attr('lineColor', line_color)

        # fill
        fill = self.data['fills'][0]
        color = fill['color']
        self.set_attr('fillColor', to_hex(color['r'], color['g'], color['b'], color['a']))

        # 圆角
        if 'cornerRadius' in self.data:
            self.set_attr('corner', self.data['cornerRadius'])
        else:
            self.set_attr('corner', 0)