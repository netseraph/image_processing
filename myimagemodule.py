"""图片操作常用工具"""

from typing import Any
from PIL import Image, ImageFont, ImageDraw


def gray_luma(red: int, green: int, blue: int) -> int:
    """加权平均法计算灰度"""
    # 加权平均法 (Luma / Perception Method):
    # 这是最常用的方法，考虑了人眼对不同颜色的敏感度。常用公式（ITU-R BT.601）：
    # Gray = 0.299*R + 0.587*G + 0.114*B
    gray = red * 299 / 1000 + green * 587 / 1000 + blue * 114 / 1000
    # print(gray)
    return int(gray)


def gray_luminance(red: int, green: int, blue: int) -> int:
    """心理学亮度计算灰度"""
    # 心理学亮度 (Luminance):在某些高级算法中（如 BT.709）
    # Gray = 0.2126*R + 0.7152*G + 0.0722*B
    gray = red * 2126 / 10000 + green * 7152 / 10000 + blue * 722 / 10000
    # print(gray)
    return int(gray)


def convert_to_signature(image_object: Any, threshold: int = 128):
    """将图片对象转换成签名样式"""

    if image_object.mode != "RGBA":
        # 给图片增加Alpha通道
        image_object = image_object.convert("RGBA")

    _size = image_object.size

    for i in range(_size[0]):
        for j in range(_size[1]):
            _pixel_color = image_object.getpixel((i, j))
            _red = _pixel_color[0]
            _green = _pixel_color[1]
            _blue = _pixel_color[2]
            _gray = gray_luma(_red, _green, _blue)

            if _gray > threshold:
                # 保留较浅的，设置为透明
                _new_pixel_color = (0, 0, 0, 0)
            else:
                # 保留较深的，设置为纯黑色
                _new_pixel_color = (0, 0, 0, 255)

            image_object.putpixel((i, j), _new_pixel_color)

    return image_object


def bw_image(imagefilename, targetimagefilenamr):
    """图片改成黑白"""
    _img = Image.open(imagefilename)
    _img = _img.convert("RGBA")
    for i in range(_img.size[0]):
        for j in range(_img.size[1]):
            _color = _img.getpixel((i, j))
            print(_color)
            if _color != (0, 0, 0, 0):
                _img.putpixel((i, j), (255, 255, 255, 0))
    _img.save(targetimagefilenamr)


def showimgattributes(image_object):
    """显示图片属性"""
    print("Image Size:", image_object.size)
    print("Image Mode:", image_object.mode)
    print("Image Format:", image_object.format)
    print("Image Info:", image_object.info)
    print("Image Palette", image_object.palette)


def showimg(filename):
    """显示图片"""
    img = Image.open(filename)
    # show image
    showimgattributes(img)
    # print(img.verify())
    img.show()


def rotateimage(filename):
    """旋转图片45度"""
    img = Image.open(filename)
    img = img.rotate(45)
    print("Image Size:", img.size)
    img.show()


def rotateimage2(filename):
    """旋转图片10度"""
    img = Image.open(filename)
    r = 10
    for _ in range(int(360 / r) + 1):
        img = img.rotate(r)
    img.show()


def rotateimage3(filename):
    """旋转图片"""
    img = Image.open(filename)
    x = img.size[0]
    y = img.size[1]
    z = int((x**2 + y**2) ** 0.5) + 1

    new_size = (z, z)
    new_rgba_img = Image.new("RGBA", new_size, (255, 255, 255))
    showimgattributes(new_rgba_img)
    # new_rgba_img.show()

    new_rgb_img = Image.new("RGB", new_size, (255, 255, 255))
    showimgattributes(new_rgb_img)
    new_rgb_img.show()


def add_watermarker(original_image_path, target_image_path, scale, watermarker_text):
    """给添加水印"""

    # print(target_image_path)

    ori_img = Image.open(original_image_path)
    print("original imange size", ori_img.size)

    font_size = int(ori_img.size[1] / scale)
    print("watermarker font size", font_size)
    font = ImageFont.truetype("SIMYOU.TTF", font_size)

    # 添加背景
    new_img = Image.new(
        "RGBA", (ori_img.size[0] * 3, ori_img.size[1] * 3), (0, 0, 0, 0)
    )
    new_img.paste(ori_img, ori_img.size)

    # 添加水印
    font_len = len(watermarker_text)
    print(font_len)
    rgba_image = new_img.convert("RGBA")
    text_overlay = Image.new("RGBA", rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    for i in range(0, rgba_image.size[0], font_len * 40 + 100):
        for j in range(0, rgba_image.size[1], 200):
            image_draw.text((i, j), watermarker_text, font=font, fill=(0, 0, 0, 50))
    text_overlay = text_overlay.rotate(-45)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)

    # 裁切图片
    image_with_text = image_with_text.crop(
        (ori_img.size[0], ori_img.size[1], ori_img.size[0] * 2, ori_img.size[1] * 2)
    )
    #
    # image_with_text.show()
    image_with_text.save(target_image_path)


def traversal_color(imagefilename: str):
    """遍历图片中每个像素的颜色"""

    _img = Image.open(imagefilename)
    for i in range(_img.size[0]):
        for j in range(_img.size[1]):
            _color = _img.getpixel((i, j))
            print(_color)


if __name__ == "__main__":
    traversal_color("test2.bmp")
