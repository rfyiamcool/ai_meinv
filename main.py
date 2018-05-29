# -*- coding: utf-8 -*-
import sys

from PIL import Image


if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)

try:
    import api
    from config import APP_ID, APP_KEY, FACE_PATH
    from compress import resize_image
except Exception as ex:
    print(ex)
    exit(1)


BEAUTY_THRESHOLD = 80


def main():
    """
    main
    :return:
    """
    while True:
        print("> input image file")
        s = input()
        if s == "":
            continue

        resize_image(s, 'optimized.png', 1024 * 1024)

        with open('optimized.png', 'rb') as bin_data:
            image_data = bin_data.read()

        ai_obj = api.AiPlat(APP_ID, APP_KEY)
        rsp = ai_obj.face_detectface(image_data, 0)

        if rsp['ret'] == 0:
            beauty = 0
            for face in rsp['data']['face_list']:
                print(face)
                face_area = (
                    face['x'],
                    face['y'],
                    face['x'] + face['width'],
                    face['y'] + face['height']
                )
                print(face_area)
                img = Image.open("optimized.png")
                cropped_img = img.crop(face_area).convert('RGB')
                cropped_img.save(FACE_PATH + face['face_id'] + '.png')
                # 性别判断
                if face['beauty'] > beauty and face['gender'] < 50:
                    beauty = face['beauty']

            # 是个美人儿~关注点赞走一波
            if beauty > BEAUTY_THRESHOLD:
                print('发现漂亮妹子！！！')
                thumbs_up()
                follow_user()

        else:
            print(rsp)
            continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
