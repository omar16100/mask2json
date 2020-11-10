'''
lanhuage: python
Descripttion: 
version: beta
Author: xiaoshuyui
Date: 2020-10-26 10:14:35
LastEditors: xiaoshuyui
LastEditTime: 2020-11-10 11:45:41
'''
import gc

from convertmask.utils.auglib.optional.Operator import (CropOperator,
                                                        DistortOperator,
                                                        InpaintOperator,
                                                        PerspectiveOperator,
                                                        ResizeOperator)
from convertmask.utils.methods.logger import logger


class MainOptionalOperator(object):
    def __init__(self, img_or_path) -> None:
        self.imgs = img_or_path
        self.defaults = ['crop', 'distort', 'inpaint', 'perspective', 'resize']
        self.augs = []
        self.operations = []

    def _help(self):
        print('========= HELP INFORMATION =========')

    def addAugs(self, method: str):
        self.augs.append(method)

    def setCropAttributes(self, **kwargs):
        if 'crop' not in self.augs:
            self.augs.append('crop')
        rect_or_poly = kwargs.get('rect_or_poly', 'rect')
        noise = kwargs.get('noise', True)
        cropNumber = kwargs.get('number', 1)
        convexHull = kwargs.get('convex', False)
        self.operations.append(
            CropOperator(None, None, rect_or_poly, noise, convexHull,
                         cropNumber))

    def setDisortAttributes(self):
        if 'distort' not in self.augs:
            self.augs.append('distort')
        self.operations.append(DistortOperator(None))

    def setInpaintAttributes(self, **kwargs):
        if 'inpaint' not in self.augs:
            self.augs.append('inpaint')
        rect_or_poly = kwargs.get('rect_or_poly', 'rect')
        startPoint = kwargs.get('start', None)
        self.operations.append(InpaintOperator(None, rect_or_poly, startPoint))

    def setPerspectiveAttributes(self, **kwargs):
        if 'perspective' not in self.augs:
            self.augs.append('perspective')
        factor = kwargs.get('factor', 0.5)
        self.operations.append(PerspectiveOperator(None, factor))

    def setResizeAttributes(self, **kwargs):
        if 'resize' not in self.augs:
            self.augs.append('resize')
        heightFactor = kwargs.get('height', 1.0)
        widthFactor = kwargs.get('width', 1.0)
        self.operations.append(ResizeOperator(None, heightFactor, widthFactor))

    def do(self):
        if len(self.augs) == 0:
            logger.info('None methods founds')
            return

        pimgs = self.imgs
        # print(pimgs)
        for i in self.operations:
            i.setImgs(pimgs)
            pimgs = i.do()
            gc.collect()

        return pimgs
