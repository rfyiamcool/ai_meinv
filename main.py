# -*- coding: utf-8 -*-
import sys
import json

import requests
from PIL import Image


try:
    import api
    from config import APP_ID, APP_KEY, FACE_PATH
    from compress import resize_image
except Exception as ex:
    print(ex)
    exit(1)


BEAUTY_THRESHOLD = 60
DEFAULT_SRC_FILE = 'download.png'
OPTIMIZED_FILE = 'optimized.png'


def is_url(url):
    return url.startswith(("http", "https"))


def download_file(url, download_path):
    try:
        r = requests.get(url, stream=True, timeout=5)
        if r.status_code == 200:
            with open(download_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(e)
        return False


def main():
    """
    main
    :return:
    """
    while True:
        print('> input image file or url')
        addr = input('> ')
        addr = addr.strip()
        if addr == "":
            continue

        if is_url(addr):
            if download_file(addr, FACE_PATH + DEFAULT_SRC_FILE) == False:
                continue
            else:
                addr = FACE_PATH + DEFAULT_SRC_FILE

        resize_image(addr, OPTIMIZED_FILE, 1024 * 1024)

        with open(OPTIMIZED_FILE, 'rb') as bin_data:
            image_data = bin_data.read()

        ai_obj = api.AiPlat(APP_ID, APP_KEY)
        rsp = ai_obj.face_detectface(image_data, 0)

        if rsp['ret'] == 0:
            for face in rsp['data']['face_list']:
                del face['face_shape']  # face_shape too big
                print(json.dumps(face, indent=1))
                beauty = 0
                face_area = (
                    face['x'],
                    face['y'],
                    face['x'] + face['width'],
                    face['y'] + face['height']
                )

                img = Image.open(OPTIMIZED_FILE)
                cropped_img = img.crop(face_area).convert('RGB')
                cropped_img.save(FACE_PATH + face['face_id'] + '.png')
                # 性别判断
                if face['gender'] < 20 and face['beauty'] > BEAUTY_THRESHOLD:
                    # detail api: https://ai.qq.com/doc/detectface.shtml
                    print('发现漂亮妹子！ 岁数: %s, 魅力值: %s'%(face['age'], face['beauty']))

                if face['gender'] > 70:
                    print('是个大老爷们, 不解释...')

                if face['gender'] >= 20 and face['gender'] <= 70:
                    print('不男不女, 不解释...')

        else:
            print("识别异常")
            print(rsp)
            continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
