"""Report editability and layout structure of a DOCX without rendering it."""

import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
NS = {'w': W, 'm': M, 'wp': WP}


def inspect(path):
    with ZipFile(path) as package:
        bad_member = package.testzip()
        if bad_member:
            raise ValueError(f'Corrupt package member: {bad_member}')
        root = ET.fromstring(package.read('word/document.xml'))
        paragraphs = root.findall('.//w:body/w:p', NS)
        text = ''.join(node.text or '' for node in root.findall('.//w:t', NS))
        display = []
        for para in paragraphs:
            if para.find('./m:oMathPara', NS) is not None or para.find('./m:oMath', NS) is not None:
                plain = ''.join(node.text or '' for node in para.findall('./w:r/w:t', NS))
                if re.search(r'\(\d+(?:-\d+)+\)', plain):
                    display.append(plain.strip())
        page = root.find('.//w:sectPr/w:pgSz', NS)
        margins = root.find('.//w:sectPr/w:pgMar', NS)
        def attrs(node):
            return {key.rsplit('}', 1)[-1]: value for key, value in node.attrib.items()} if node is not None else {}
        return {
            'file': str(path),
            'paragraphs': len(paragraphs),
            'editable_text_characters': len(text),
            'native_math_objects': len(root.findall('.//m:oMath', NS)),
            'numbered_equation_paragraphs': len(display),
            'equation_labels': [re.search(r'\(\d+(?:-\d+)+\)', x).group() for x in display],
            'inline_images': len(root.findall('.//wp:inline', NS)),
            'anchored_images': len(root.findall('.//wp:anchor', NS)),
            'page_size_twips': attrs(page),
            'page_margins_twips': attrs(margins),
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('docx', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.docx), ensure_ascii=False, indent=2))
