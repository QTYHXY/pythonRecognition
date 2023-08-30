from os import path
from tkinter import *
from aip import *
from PIL import Image, ImageTk

import tkinter.filedialog
import base64
import cv2


def setInterface() -> tkinter.Tk:
    '''
    界面设置
    :return: 界面
    '''
    # 新建Tk对象
    interface = tkinter.Tk()
    # 设置标题
    interface.title('霍新宇的识别小程序')
    # 设置界面大小
    interface.geometry('600x600')
    return interface


def displayInterface(interface) -> bool:
    # disabled
    '''
    图片位置设置
    :param interface: 界面
    :return: Bool
    '''
    lab = Label(master=interface)
    lab.place(relx=0.4, rely=0.48)
    return True


def displayKey(interface) -> None:
    '''
    按键设置和布局
    :param interface: 界面
    :return: None
    '''
    # 按键
    butAnimal = tkinter.Button(master=interface, text='动物识别', background='#c86b41', foreground='WHITE',
                               command=lambda: recognition(1))
    butDish = tkinter.Button(master=interface, text='菜品识别', background='#c86b41', foreground='WHITE',
                             command=lambda: recognition(2))
    butPlant = tkinter.Button(master=interface, text='植物识别', background='#c86b41', foreground='WHITE',
                              command=lambda: recognition(3))
    butingre = tkinter.Button(master=interface, text='果蔬识别', background='#c86b41', foreground='WHITE',
                              command=lambda: recognition(4))

    butQrcode = tkinter.Button(master=interface, text='二维码识别', background='#82da98', foreground='WHITE',
                               command=lambda: textRecognition(1))
    butHandWriting = tkinter.Button(master=interface, text='手写识别', background='#82da98', foreground='WHITE',
                                    command=lambda: textRecognition(2))

    butShoot = tkinter.Button(master=interface, text='拍照并上传', background='#3483f4', foreground='WHITE',
                              command=lambda: pictureShoot())

    butFaceMatch = tkinter.Button(master=interface, text='人脸对比', background='#3483f4', foreground='WHITE',
                                  command=lambda: faceMatchInterface(interface, 0))
    butFaceDetection = tkinter.Button(master=interface, text='人脸检测', background='#3483f4', foreground='WHITE',
                                      command=lambda: faceRecognition())
    buttonSelImage = tkinter.Button(interface, text='选择图片', command=displayPictures)
    buttonCloseMain = tkinter.Button(interface, text='  退 出  ', background='#1e1f22', foreground='RED',
                                     command=lambda: closeInterface(interface), )
    # 按键位置
    butAnimal.place(relx=0.5, rely=0.7)
    butDish.place(relx=0.3, rely=0.7)
    butPlant.place(relx=0.3, rely=0.85)
    butingre.place(relx=0.5, rely=0.85)
    butQrcode.place(relx=0.7, rely=0.85)
    butHandWriting.place(relx=0.1, rely=0.77)
    butShoot.place(relx=0.7, rely=0.7)
    butFaceMatch.place(relx=0.1, rely=0.85)
    butFaceDetection.place(relx=0.1, rely=0.7)
    buttonSelImage.place(relx=0.44, rely=0.4)
    buttonCloseMain.place(relx=0.1, rely=0.55)


def closeInterface(interface) -> bool:
    '''
    关闭窗口
    :param interface: 界面
    :return: Bool
    '''
    askokcancel = tkinter.messagebox.askokcancel(title='是否要执行该操作', message='是否要退出程序')
    if askokcancel:
        interface.destroy()
    return True


def faceMatchInterface(myinterface, msg) -> bool:
    '''
    启用人脸对比界面
    :param interface: 界面
    :param msg: 启动和隐藏
    :return: bool
    '''
    # 设置人脸匹配界面
    root = tkinter.Toplevel()
    # 设置界面标题
    root.title('霍新宇的人脸匹配')
    # 设置界面大小
    root.geometry('600x600')
    # 启用人脸匹配按钮
    buttonStart = tkinter.Button(root, text='开始匹配', background='#3483f4', foreground='WHITE',
                                 command=lambda: faceMatch(root))
    # 人脸匹配按钮位置设置
    buttonStart.place(relx=0.44, rely=0.5)
    # 退出
    buttonCloseroot = tkinter.Button(root, text='  退 出  ', background='#1e1f22', foreground='RED',
                                     command=lambda: closeInterface(root))
    # 退出按钮位置设置
    buttonCloseroot.place(relx=0.44, rely=0.8)

    if msg == 0:
        # 启用人脸匹配
        print("准备开始人脸匹配")
        faceMatchMainInterface(root)
        root.mainloop()
    else:
        # 隐藏人脸匹配
        root.withdraw()
        print("人脸匹配界面关闭成功")
    return True


def faceMatchMainInterface(myinterface) -> bool:
    '''
    人脸对比界面设置
    :param myinterface:界面
    :return:Bool
    '''
    # 提示按钮设置1
    buttonSelImage = tkinter.Button(myinterface, text='选择两张图片', command=displayPictures, state='disabled')
    # 按钮位置设置
    buttonSelImage.place(relx=0.42, rely=0.4)

    # 使用Label显示图片1
    lableFaceMacth1 = tkinter.Label(myinterface)
    # 图片1显示的位置设置
    lableFaceMacth1.place(relx=0.05, rely=0.05)

    # 选择图片1按钮设置 绑定事件
    buttonSelImage1 = tkinter.Button(myinterface, text='选择图片1', background='#c86b41', foreground='WHITE',
                                     command=lambda: faceMatchChoosePic(lableFaceMacth1))
    # 选择图片1按钮位置设置
    buttonSelImage1.place(relx=0.15, rely=0.4)

    # 使用Label显示图片2
    lableFaceMacth2 = tkinter.Label(myinterface)
    # 图片2显示的位置设置
    lableFaceMacth2.place(relx=0.6, rely=0.05)

    # 选择图片2按钮设置 绑定事件
    buttonSelImage2 = tkinter.Button(myinterface, text='选择图片2', background='#c86b41', foreground='WHITE',
                                     command=lambda: faceMatchChoosePic(lableFaceMacth2))
    # 选择图片2按钮位置设置
    buttonSelImage2.place(relx=0.7, rely=0.4)

    return True


def faceMatch(root) -> bool:
    '''
    人脸对比
    :return:Bool
    '''
    # 打开路径文件，读取路径
    try:
        fileRead = open('path.txt')
    except:
        print("打开失败")
    else:
        # 读取路径文件
        content = fileRead.read()
        # 分割路径文件
        contentSplit = content.split("*")
        print(f'路径文件内容是{content}')
        print(f'分割完成的内容是{contentSplit}')
    finally:
        # 清空路径文件
        file = open("path.txt", 'w').close()
        fileRead.close()

    # 显示文本1的初始化对象和位置
    labText1 = Label(master=root)
    labText1.place(relx=0.44, rely=0.6)

    # 显示文本2的初始化对象和位置
    labText2 = Label(master=root)
    labText2.place(relx=0.4, rely=0.63)

    # 显示文本3的初始化对象和位置
    labText3 = Label(master=root)
    labText3.place(relx=0.4, rely=0.66)

    im1 = contentSplit[0]
    im2 = contentSplit[1]
    # 调用aipFace
    appid = '34541638'
    aipkey = 'tUNMQWpiGXe5mg24pTiytkK1'
    secrectkey = 'T8jYuAGN0l4jKz258MUI9o3o6HvMkQmC'
    client = AipFace(appid, aipkey, secrectkey)
    # 打开与读取图片
    image1 = open(im1, 'rb').read()
    image2 = open(im2, 'rb').read()
    # 对图片进行编码，上传到云端分析
    result = client.match([{'image': str(base64.b64encode(image1), 'utf-8'),
                            'image_type': 'BASE64'},
                           {'image': str(base64.b64encode(image2), 'utf-8'),
                            'image_type': 'BASE64'}, ])
    # 打印结果
    print(result)
    similarity = result['result']['score']
    if result['error_code'] == 0:
        labText1.configure(text='匹配完成')
        labText2.configure(text=f'相似度是{similarity}%')
        if similarity > 90:
            labText3.configure(text=f'相似度很高，是同一个人')
        elif similarity > 70:
            labText3.configure(text=f'相似度还是比较高的，可能是同一个人')
        else:
            labText3.configure(text=f'相似度较低，无法判定是同一个人')

    if result['result'] != None:
        print('%s和%s' % (im1, im2) + '相似度是%.2f'
              % similarity + '%')
        if similarity >= 90:
            print('%s和%s' % (im1, im2) + '相似度很高，是同一个人')
        else:
            print('%s和%s' % (im1, im2) + '相似度较低，无法判定是同一个人')
    return True


def faceMatchChoosePic(lableFaceMacth) -> bool:
    '''
    人脸匹配的照片选择
    :param lableFaceMacth:
    :return:
    '''
    # 打开文件选择
    pathFaceMatch = tkinter.filedialog.askopenfilename()
    # 保存路径
    try:
        fileSave = open('path.txt', 'a+')
    except:
        print("打开失败")
    else:
        print("打开文件成功")
        fileSave.write(pathFaceMatch + '*')
    finally:
        fileSave.close()
    # 获取图片
    img_open = Image.open(pathFaceMatch)
    # 设置显示图片大小
    img = ImageTk.PhotoImage(img_open.resize((200, 200)))
    # 显示图片
    lableFaceMacth.config(image=img)
    lableFaceMacth.image = img
    return True


def displayPath(interface) -> tkinter.Entry:
    '''
    输入框的路径显示
    :return:entry控件
    '''
    # 转化格式
    path = tkinter.StringVar()
    # 设置输入框
    entry = tkinter.Entry(interface, state='readonly', text=path, width=100)
    # 启用输入框
    entry.pack()
    return path, entry


def displayPictures() -> bool:
    '''
    图片显示
    :return: Bool
    '''
    # 输入框共享路径
    global pathShow
    # 打开文件选择
    pathShow = tkinter.filedialog.askopenfilename()
    # 把路径显示在输入框
    path.set(pathShow)
    # 获取输入框路径
    img_open = Image.open(entry.get())
    # 设置图片显示大小
    img = ImageTk.PhotoImage(img_open.resize((200, 200)))
    # 显示图片
    lableShowImage.config(image=img)
    lableShowImage.image = img
    return True


def recognition(msg) -> int:
    '''
    图片识别区域
    :param msg: 选择识别类型
    :return: 识别类型
    '''
    # 显示名字文本的初始化对象和位置
    labTextName = Label(master=interface)
    labTextName.place(relx=0.4, rely=0.48)

    # 显示置信度文本的初始化对象和位置
    labTextScore = Label(master=interface)
    labTextScore.place(relx=0.4, rely=0.52)

    # 显示置信度文本的初始化对象和位置
    labTextDescriptionMore = Label(master=interface)
    labTextDescriptionMore.place(relx=0.4, rely=0.56)

    # 显示细节文本的初始化对象和位置
    labTextDescription = Label(master=interface, justify=CENTER)
    labTextDescription.place(relx=0.4, rely=0.6)

    options = {}
    options["top_num"] = 3
    options["baike_num"] = 2

    APP_ID = '34289199'
    API_KEY = 'W6w2pnvv5WSgbruUdwc4L8DG'
    SECRET_KEY = 'vBhCWDUTjE6eqlzqExm8tB4QGW4CGQR9'
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    # 异常判断
    try:
        file = open(pathShow, 'rb')
    except Exception as e:
        labTextName.configure(text='路径错误或不存在        ')
        print("路径错误或不存在")
    else:
        image = file.read()
        # 动物识别
        if msg == 1:
            # 动物检测
            result = client.animalDetect(image, options)
            name = result.get('result')[0].get('name')
            labTextName.configure(text=f'动物名称：{name}                    ')
            print(f'动物名称{name}')
            score = result.get('result')[0].get('score')
            labTextScore.configure(text=f'置信度：{score}                      ')
            print(f'置信度：{score}')
            if float(score) > 0.9:
                labTextDescriptionMore.configure(text='置信度在可信范围内                ')
            else:
                labTextDescriptionMore.configure(text='置信度过低                       ')
            description = result.get('result')[0].get('baike_info').get('description')
            # labTextDescription.configure(text=f'百度百科介绍：{description}       ')
            print(f'百度百科介绍：{description}')
            return 1
        # 菜品识别
        elif msg == 2:
            # 菜品检测
            result = client.dishDetect(image, options)
            name = result.get('result')[0].get('name')
            labTextName.configure(text=f'菜品名称：{name}                   ')
            print(f'菜品名称{name}')
            score = result.get('result')[0].get('score')
            labTextScore.configure(text=f'置信度：{score}                 ')
            print(f'置信度：{score}')
            labTextDescriptionMore.configure(text='检测完成                             ')
            description = result.get('result')[0].get('baike_info').get('description')
            # labTextDescription.configure(text=f'百度百科介绍：{description}       ')
            print(f'百度百科介绍：{description}')
            return 2
        elif msg == 3:
            # 植物检测
            result = client.plantDetect(image, options)
            name = result.get('result')[0].get('name')
            labTextName.configure(text=f'植物名称：{name}                                 ')
            print(f'植物名称{name}')
            score = result.get('result')[0].get('score')
            labTextScore.configure(text=f'置信度：{score}                             ')
            print(f'置信度：{score}')
            if float(score) > 0.9:
                labTextDescriptionMore.configure(text='置信度在可信范围内                         ')
            else:
                labTextDescriptionMore.configure(text='置信度过低                                  ')
            description = result.get('result')[0].get('baike_info').get('description')
            # labTextDescription.configure(text=f'百度百科介绍：{description}       ')
            print(f'百度百科介绍：{description}')
            return 3
        elif msg == 4:
            # 果蔬检测
            result = client.ingredient(image, options)
            name = result.get('result')[0].get('name')
            labTextName.configure(text=f'果蔬名称：{name}                    ')
            print(f'果蔬名称{name}')
            score = result.get('result')[0].get('score')
            labTextScore.configure(text=f'置信度：{score}                 ')
            print(f'置信度：{score}')
            if float(score) > 0.9:
                labTextDescriptionMore.configure(text='置信度在可信范围内              ')
            else:
                labTextDescriptionMore.configure(text='置信度过低                       ')
            # labTextDescription.configure(text=f'百度百科介绍：{description}       ')
            return 3
    finally:
        file.close()


def pictureShoot(image_name='shootImg.png', image_path=r'data') -> bool:
    '''
    调用摄像头拍照并保存图片到本地
    :param image_name: 图片名字
    :param image_path: 图片保存路径
    :return: None
    '''
    # 显示文本的初始化对象和位置
    labText = Label(master=interface, height=7, width=40)
    labText.place(relx=0.3, rely=0.48)

    global pathShow
    # 启用默认摄像头
    cap = cv2.VideoCapture(0)
    # 确定摄像头是否成功
    while (cap.isOpened()):
        # 是否成功and帧数
        ret, frame = cap.read()
        # cv2.imshow("Capture_Paizhao", frame) # 显示窗口
        # 保存图片
        cv2.imwrite(image_path + "\\" + image_name, frame)
        print("保存" + image_name + "成功!")
        labText.configure(text='        拍摄完成                        ')
        break
    # 全局变量记住路径
    pathShow = 'data/shootImg.png'
    path.set(pathShow)
    # 显示图片
    img_open = Image.open('data/shootImg.png')
    img = ImageTk.PhotoImage(img_open.resize((200, 200)))
    lableShowImage.config(image=img)
    lableShowImage.image = img
    return True


def faceRecognition() -> bool:
    '''
    人脸检测并上传
    :return: Bool
    '''
    global pathShow
    # 显示文本的初始化对象和位置
    labText = Label(master=interface, height=7, width=40)
    labText.place(relx=0.32, rely=0.48)
    # 读取图片
    img = cv2.imread(pathShow)
    # 灰度转换
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 导入识别方法
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_detector.detectMultiScale(gray)
    # 画出人脸位置
    for x, y, w, h in faces:
        # 圈出来
        cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
        cv2.circle(img, center=(x + w // 2, y + h // 2), radius=w // 2, color=(0, 255, 255), thickness=2)
    # 保存识别后的图片和路径
    cv2.imwrite('data/faceRecognition.png', img)
    img_open = Image.open('data/faceRecognition.png')
    pathShow = 'data/faceRecognition.png'
    # 显示路径
    path.set(pathShow)
    # 设置显示图片大小
    img = ImageTk.PhotoImage(img_open.resize((200, 200)))
    # 显示图片
    lableShowImage.config(image=img)
    lableShowImage.image = img
    print("检测完成")
    labText.configure(text='                检测完成                              ')
    return True


def textRecognition(msg)->int:
    '''
    文字识别部分
    :param msg: 选择识别类型
    :return: 识别类型
    '''
    APP_ID = '35195194'
    API_KEY = 'Z8mroP8RTx1cni5ARHIK9shj'
    SECRET_KEY = 'Wq1mKIxpEoGE40YpNrII8uNWSaguhbbR'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    # 显示名字文本的初始化对象和位置
    labTextName = Label(master=interface)
    labTextName.place(relx=0.4, rely=0.48)

    # 显示置信度文本的初始化对象和位置
    labTextScore = Label(master=interface)
    labTextScore.place(relx=0.4, rely=0.52)

    # 显示置信度文本的初始化对象和位置
    labTextDescriptionMore = Label(master=interface)
    labTextDescriptionMore.place(relx=0.4, rely=0.56)

    # 显示细节文本的初始化对象和位置
    labTextDescription = Label(master=interface, justify=CENTER)
    labTextDescription.place(relx=0.4, rely=0.6)

    try:
        file = open(pathShow, 'rb')
    except Exception as e:
        labTextName.configure(text='路径错误或不存在                       ')
        print("路径错误或不存在")
    else:
        image = file.read()
        if msg == 1:
            result = client.qrcode(image, options)
            info = result['codes_result'][0]['text']
            for result in result['codes_result'][0]['text']:
                print(result)
            labTextName.configure(text=f'{info}                                ')
            labTextScore.configure(text='                                       ')
            labTextDescriptionMore.configure(text='                                     ')
            labTextDescription.configure(text='                                     ')
            return 1
        if msg == 2:
            result = client.handwriting(image, options)
            print(result)
            keywordList = list()
            for keyword in result['words_result']:
                keywordList.append(keyword['words'])
                print(keyword['words'])
            print(keywordList)
            labTextName.configure(text=f'{keywordList[1]}                                ')
            labTextScore.configure(text=f'{keywordList[2]}                                       ')
            labTextDescriptionMore.configure(text=f'{keywordList[3]}                                     ')
            return 2
    finally:
        file.close()


if __name__ == '__main__':
    # 界面初始化
    interface = setInterface()
    # 界面展示
    displayInterface(interface)
    # 按键展示
    displayKey(interface)
    # 路径展示
    path, entry = displayPath(interface)
    # 使用Label显示图片
    lableShowImage = tkinter.Label(master=interface)
    lableShowImage.pack()
    # 页面启动

    interface.mainloop()
