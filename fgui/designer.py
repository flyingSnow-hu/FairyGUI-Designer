import os
from typing import Dict, List
from xml.dom.minidom import Document, Element

import tkdesigner.figma.endpoints as endpoints
from fgui.Group import Group
from fgui.Image import Image
from fgui.Shape import Shape
from fgui.Text import Text
from fgui.utils import get_id_hash

class Designer:
    def __init__(self, token, file_key, output_path: str):
        self.output_path = output_path
        self.figma_file = endpoints.Files(token, file_key)
        self.file_data = self.figma_file.get_file()
        print(self.file_data)
        self.frameCounter = 0

        self.package_doc = None
        self.resources_node = None

        self.asset_nodes: List[tuple[tuple[str, str],...]] = []

    def to_code(self):
        if 'err' in self.file_data:
            print(f'网络错误：{self.file_data['status']}')
            return

        # 这个 page 是 figama 的 page，相当于 fgui 的 package
        for page in self.file_data['document']['children']:
            # component_names = []

            self.create_package_node(page)
            # figma 的 layer，相当于 fgui 的 component
            for layer in page['children']:
                element = self.package_doc.createElement("component")
                element.setAttribute("id", get_id_hash(layer['id']))
                element.setAttribute("name", f"{layer['name']}.xml")
                element.setAttribute("path", "/")
                element.setAttribute("exported", "true")
                self.resources_node.appendChild(element)
                self.decode_package(layer, page)

            self.write_package(page['name'])

    @staticmethod
    def write_xml(xml:Document, file_path:str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, encoding='UTF-8', mode='w') as w:
            w.write(xml.toprettyxml(encoding='UTF-8').decode('utf-8'))

    def decode_package(self, layer, page:Dict):
        package_name = page['name']

        component_name = layer['name']
        bounding = layer['absoluteBoundingBox']
        layer_x, layer_y, layer_width, layer_height = bounding['x'], bounding['y'], int(bounding['width']), int(bounding['height'])

        # xml root
        doc = Document()
        root = doc.createElement('component')
        root.setAttribute('size', f'{layer_width},{layer_height}')
        root.setAttribute('bgColorEnabled', "true")
        doc.appendChild(root)

        display_list = doc.createElement('displayList')
        root.appendChild(display_list)

        # add components to package.xml
        # for component in page['children']:
        #     element = self.package_doc.createElement("component")
        #     element.setAttribute("id", get_id_hash(component['id']))
        #     element.setAttribute("name", f"{component['name']}.xml")
        #     element.setAttribute("path", "/")
        #     element.setAttribute("exported", "true")
        #     self.resources_node.appendChild(element)

        self.add_display_node(display_list, doc, layer, layer_x, layer_y, package_name)

        output_path = os.path.join(self.output_path, package_name, f'{component_name}.xml')
        Designer.write_xml(doc, output_path)

    def add_display_node(self, display_list:Element, doc:Document, layer:Dict, layer_x:int, layer_y:int, package_name:str, group_id:str=None):
        for node in layer['children']:
            element, decoder = None, None
            colon_pos = str(node['name']).rfind(':')
            if colon_pos <= 0 or colon_pos >= len(node['name']) - 1:
                print(f'不认识这个东西：{node['name']} / {node['type']}')
                continue

            (name, type_) = node['name'][:colon_pos], node['name'][colon_pos+1:]
            if type_ == 'Shape':
                element = doc.createElement('graph')
                decoder = Shape(node, element)
            elif type_ == 'Richtext':
                element = doc.createElement('richtext')
                decoder = Text(node, element)
            elif  type_ == 'Text' or  type_ ==  'Input':
                element = doc.createElement('text')
                decoder = Text(node, element)
            elif  type_ == 'Image':
                element = doc.createElement('image')
                decoder = Image(node, element, self.figma_file, os.path.join(self.output_path, package_name))
            elif  type_ == 'Group':
                element = doc.createElement('group')
                decoder = Group(node, element)
                self.add_display_node(display_list, doc, node, layer_x, layer_y, package_name, group_id=decoder.id)
            else:
                print(f'不认识这个东西：{node['name']} / {node['type']}')
                continue

            if group_id is not None:
                decoder.set_group_id(group_id)
            decoder.set_offset(-layer_x, -layer_y)
            decoder.decode(self.asset_nodes)

            asset_ele = decoder.add_to_package(doc)
            while asset_ele is not None:
                # print(f'add {element}')
                self.resources_node.appendChild(asset_ele)
                asset_ele = decoder.add_to_package(doc)

            print(f'添加 {node['name']}')
            display_list.appendChild(element)

    def create_package_node(self, package:Dict):
        """
        创建 package.xml
        """
        # 创建文档对象
        self.package_doc = Document()

        # 创建根节点
        root = self.package_doc.createElement("packageDescription")
        root.setAttribute("id", get_id_hash(package['id']))
        self.package_doc.appendChild(root)

        # 创建 resources 节点
        self.resources_node = self.package_doc.createElement("resources")
        root.appendChild(self.resources_node)

        # 创建 publish 节点
        publish = self.package_doc.createElement("publish")
        publish.setAttribute("name", "")
        root.appendChild(publish)

    def write_package(self, package_name:str):
        # # 创建 component 节点
        # for layer in package['children']:
        #     component = self.package_doc.createElement("component")
        #     component.setAttribute("id", get_id_hash(layer['id']))
        #     component.setAttribute("name", f"{layer['name']}.xml")
        #     component.setAttribute("path", "/")
        #     component.setAttribute("exported", "true")
        #     resources.appendChild(component)
        #
        # # 添加资源
        # for asset in self.asset_nodes:
        #     element = self.package_doc.createElement("image")
        #     for name, value in asset:
        #         element.setAttribute(name, value)
        #     resources.appendChild(element)

        output_path = os.path.join(self.output_path, package_name, f'package.xml')
        Designer.write_xml(self.package_doc, output_path)
