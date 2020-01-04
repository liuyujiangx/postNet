import base64
import json
import os
from PIL import Image
from app import api, db
from . import home
from flask import request, Response, render_template
from flask_restful import Resource, fields, marshal_with

basedir = 'C:\\Users\\19145\\PycharmProjects\\postNet\\app\\static'


@home.route('/')
def index():
    return 'hello word!!'


@home.route('/img_base64', methods=['post'])
def Img_base64():
    img_base64 = request.form.get('url')
    print(img_base64)
    return img_base64


@home.route('/upload', methods=['post'])
def Upload():
    img = request.files.get('photo')
    img_list = ['img', 'png', 'IMG', 'PNG', 'jpg', 'JPG']
    if img.filename[-3:] or img.filename[-4:] in img_list:
        path = basedir + "/images/"
        file_path = path + img.filename
        file_name = img.filename
        img.save(file_path)  # 保存图片
        img_compress(file_path, file_path)  # 压缩图片
        img = Image.open(file_path)  # 获得图片宽高
        img_width = img.width
        img_height = img.height
        file_pathx = 'images/' + file_name
    else:
        img_width = 512
        img_height = 343
        file_pathx = 'images/8e94724aaac54443a3c180b264fbd74d.jpg'
        print('上传图片错误,使用默认图片')

    return render_template('index.html', img_width=img_width, img_height=img_height, file_pathx=file_pathx)


# 获取文件大小（KB）
def get_img_kb(filePath):
    # filePath图片地址（包含图片本身）
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024)

    return round(fsize, 2)


# 对图片进行压缩处理,w>512=>512
def img_compress(from_src, save_src):
    # from_src需要压缩的图片地址,save_src压缩后图片的保存地址。（地址中包含图片本身）
    img = Image.open(from_src)
    w, h = img.size
    if w > 512:
        h = h * (512 / w)
        w = w * (512 / w)

    img = img.resize((int(w), int(h)), Image.ANTIALIAS)
    img.save(save_src, optimize=True, quality=85)  # 质量为85效果最好
    if get_img_kb(save_src) > 60:
        img.save(save_src, optimize=True, quality=75)
