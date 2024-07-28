# Lenovo-"Xie Yan"
import ddddocr
from PIL import Image
import os

from tiktok_config import Verication_Tk_Dir


def ddddOcr_tk(targe_png,background_png):
    """
    :param targe_png:小图
    :param background_png: 大图
    :return: 返回目标位置左侧的距离
    """
    det = ddddocr.DdddOcr(det=False, ocr=False,show_ad=False)
    # 路径处理
    def check_png(name):
        if not name.endswith('.png'):  # 确保有后缀名
            name = "%s.png" % name
        return name
    inner_image = check_png(targe_png)
    outer_image = check_png(background_png) # 确保后缀名
    inner_png_dir = os.path.join(Verication_Tk_Dir, inner_image)
    outer_png_dir = os.path.join(Verication_Tk_Dir, outer_image) # 路径拼接
    targe_png = inner_png_dir
    background_png = outer_png_dir
    # 小图
    with open(targe_png, 'rb') as f:
        target_bytes = f.read()
    small_img = Image.open(targe_png)
    small_img_w,small_img_h  = small_img.size
    # 大图
    with open(background_png, 'rb') as f:
        background_bytes = f.read()
    background_img = Image.open(background_png)
    background_img_w,small_img_h  = background_img.size
    res = det.slide_match(target_bytes, background_bytes, simple_target=True)
    target_positon_in_need = res['target'] # background中target的位置
    target_positon_center_w = (target_positon_in_need[0]+target_positon_in_need[2])//2 # 计算中心位置
    if abs(small_img_w - (target_positon_in_need[2]- target_positon_in_need[0]))>small_img_w*0.5:
        print('the error is too big')
    return target_positon_in_need[0]