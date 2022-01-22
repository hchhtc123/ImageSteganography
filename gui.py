"""
    “秘隐”-图像隐写系统主程序
    进行图像信息隐藏及提取
"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import interface
from functools import partial
from ImageSteganography import ImageSteganography
from TextSteganography import TextSteganography
from PIL import Image
from pylab import *
from AES import AESCrypt

# 在载体图片中隐藏文本信息
def HideInformation(ui):
    inputpath = ui.lineEdit.text()          # 获取载体图片路径
    message = ui.textEdit.toPlainText()     # 获取要隐藏的私密信息
    outputpath = ui.lineEdit_2.text()       # 获取图片输出路径
    key = ui.lineEdit_4.text()              # 获取用户输入的6位密钥
    if inputpath == '' or message == '' or outputpath == '' or key == '':
        ui.label_26.setPixmap(QPixmap(""))
        ui.tip1()
    elif len(key) != 6:
        ui.label_26.setPixmap(QPixmap(""))
        ui.warn2()
    else:
        message += key
        message = cryptor.aes_encrypt(message)                    # 使用AES加密算法对要隐藏的信息进行加密
        TextSteganography.encode(inputpath, outputpath, message)  # 在图像中隐藏文本信息
        ui.showimage3()
        ui.success1()
                
# 提取图像中隐藏文本信息
def ExtractInformation(ui):
    img = ui.lineEdit_3.text()      # 获取含密图片路径
    key1 = ui.lineEdit_5.text()     # 获取用户输入密钥
    if img == '' or key1 == '':
        ui.textEdit_2.setText('')
        ui.tip1()
    elif len(key1) != 6:
        ui.textEdit_2.setText('')
        ui.warn2()
    else:
        result = TextSteganography.decode(img)      # 提取图片中隐藏的文本信息
        if (result == 0):                           # 若提取后文本信息为空提示找不到图片中隐藏信息
            ui.textEdit_2.setText('')
            ui.warn4()
        else:
            result = cryptor.aes_decrypt(result)   # 提取后使用AES算法进行解密
            if (result[-6:] == key1):              # 比对提取后的6位密钥是否与用户输入的密钥相同以判断密钥是否正确
                ui.textEdit_2.setText(str(result[:-6]))
                ui.success2()
            else:
                ui.textEdit_2.setText('')          
                ui.warn5()                          # 发出密钥错误时警告

# 在载体图片中隐藏图片
def HideImage(ui):
    image1 = ui.lineEdit_7.text()           # 获取载体图片路径
    image2 = ui.lineEdit_8.text()           # 获取要隐藏的图片路径
    outputpath1 = ui.lineEdit_10.text()     # 获取输出图片路径
    if image1 == '' or image2 == '' or outputpath1 == '':
        ui.label_29.setPixmap(QPixmap(""))
        ui.tip1()
    else:
        merged_image = ImageSteganography.merge(Image.open(image1), Image.open(image2))    # 进行图片隐藏
        if merged_image == 0:
            ui.tip4()
        else:
            merged_image.save(outputpath1)
            ui.showimage1()
            ui.tip2()

#  提取图片中隐藏私密图片
def ExtractImage(ui):
    image3 = ui.lineEdit_11.text()       # 获取要进行提取的私密图片
    outputpath2 = ui.lineEdit_13.text()  # 获取图片输出路径
    if image3 == '' or outputpath2 == '':
        ui.label_31.setPixmap(QPixmap(""))
        ui.tip1()
    else:
        unmerged_image = ImageSteganography.unmerge(Image.open(image3))  # 进行图片提取
        unmerged_image.save(outputpath2)
        ui.showimage2()
        ui.tip3()

if __name__ == '__main__':
    # 自定义设置AES对称加密16位密匙以提高信息安全性
    secretkey = 'ZGJfXxZNGPqWAC53'
    cryptor = AESCrypt(secretkey)

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = interface.Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # 文本信息隐藏按钮
    ui.pushButton_3.clicked.connect(partial(HideInformation, ui))
    # 文本信息提取按钮
    ui.pushButton_5.clicked.connect(partial(ExtractInformation, ui))
    # 图像里藏图像按钮
    ui.pushButton_15.clicked.connect(partial(HideImage, ui))
    # 提取图片中隐藏图像按钮
    ui.pushButton_19.clicked.connect(partial(ExtractImage, ui))
    
    sys.exit(app.exec_())
