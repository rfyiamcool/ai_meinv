# ai_meinv

输入一个美女照片地址，给出她的评分, 用来判定是否为高颜值的美女.

*使用腾讯ai进行人脸检测, 当然美不美主观因素太多, 概率上可以接受*

`base on https://github.com/wangshub/Douyin-Bot`

### Usage:

```
> input image file or url
/Users/xiaorui/Downloads/mm.jpeg
{
 "face_id": "2602500259781310364",
 "x": 197,
 "y": 106,
 "width": 255,
 "height": 255,
 "gender": 0,
 "age": 22,
 "expression": 43,
 "beauty": 80,
 "glass": 0,
 "pitch": 11,
 "yaw": 3,
 "roll": 14
}
发现漂亮妹子！ 岁数: 22, 魅力值: 80
> input image file or url
https://pic4.zhimg.com/80/6808a53e084fd2ef16d40442970f03ee_hd.jpg
{
 "face_id": "2602501427420002814",
 "x": 215,
 "y": 40,
 "width": 65,
 "height": 65,
 "gender": 0,
 "age": 27,
 "expression": 75,
 "beauty": 100,
 "glass": 0,
 "pitch": 16,
 "yaw": 3,
 "roll": 5
}
发现漂亮妹子！ 岁数: 27, 魅力值: 100
> input image file or url

```
