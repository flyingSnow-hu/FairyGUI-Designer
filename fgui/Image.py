import os
from typing import Dict, List
from xml.dom.minidom import Element,Document

from fgui.Decoder import ADecoder
import tkdesigner.figma.endpoints as endpoints
from fgui.utils import get_part_before_colon
from tkdesigner.utils import download_image


class Image(ADecoder):
    def __init__(self, data: Dict, node: Element, figma_file:endpoints.Files, package_dir:str):
        super().__init__(data, node)
        self.package_dir = package_dir
        self.figma_file = figma_file
        self.out_images = []

        self.out_count = 0

    def decode(self, out_assets: List[tuple[tuple[str, str],...]]):
        self._add_basic_attrs()

        img_name = get_part_before_colon(self.data['name'])
        img_id = f'i{self.id[1:]}'
        self.set_attr('src', img_id)
        self.set_attr('fileName', f'src/{img_name}.png')

        # img
        image_url = self.figma_file.get_image(self.data['id'])
        image_path = os.path.join(self.package_dir, 'src', f'{img_name}.png')

        download_image(image_url, image_path)

        #
        attrs = (('id', img_id), ('name', f'{img_name}.png'), ('path', '/src/'))
        self.out_images.append(attrs)

        # 圆角
        if 'cornerRadius' in self.data:
            self.set_attr('corner', self.data['cornerRadius'])
        else:
            self.set_attr('corner', 0)

    def add_to_package(self, package_doc:Document) -> Element|None:
        if self.out_count < len(self.out_images):
            element = package_doc.createElement('image')
            for attr, value in self.out_images[self.out_count]:
                element.setAttribute(str(attr), str(value))
            self.out_count += 1
            return element

        return None
