import base64
import threading
import pyperclip
import re
import keyboard
import time
from tkinter import *


def base64UTF8(s):
    return toBase(s, 'UTF-8')


def utf8BASE64(s):
    return fromBase(s, 'UTF-8')


def base64GBK(s):
    return toBase(s, 'GBK')


def gbkBASE64(s):
    return fromBase(s, 'GBK')


def toBase(s, encoding):
    return base64.b64encode(s.encode(encoding)).decode(encoding)


def fromBase(s, encoding):
    return base64.b64decode(s.encode(encoding)).decode(encoding)

METHOD = {
    'UTF-8': {
        'de': utf8BASE64,
        'en': base64UTF8
    },
    'GBK': {
        'de': gbkBASE64,
        'en': base64GBK
    }
}

IS_SHOW = True


def show(str):
    window = Tk()
    window.title("解密")
    msg = Message(window, text=str)
    msg.pack()
    window.minsize(200, 30)
    window.wm_attributes('-topmost', 1)
    window.mainloop()


def callMethod(str, key, type):
    for k in METHOD.keys():
        if k == key:
            return METHOD[key][type](str)
    print("不支持的加密类型")
    return None

def encode(str):
    key = re.findall('^\^(.+)$', str, re.M)
    if key:
        key = key[0].strip().upper()
        str = str[str.find('\n')+1:]
        encode = callMethod(str, key, 'en')
        if not encode:
            return
        print("开始使用", key, "加密...")
        encode = encode+"\n"+key+"$这是一条简单加密信息哦 by uyume"
        pyperclip.copy(encode)
        keyboard.press_and_release('ctrl+v')
        print("加密完毕")


def decode(str):
    key = re.findall('^(.+)\$.*$', str, re.M)
    if key:
        key = key[0].strip().upper()
        str = str[:str.find(key+'$')]
        decode = callMethod(str, key, 'de')
        if not decode:
            return
        print("开始使用", key, "解密...")
        decode = "^"+key+"\n"+decode
        if IS_SHOW:
            th = threading.Thread(target=show, args=(decode,))
            th.daemon = True
            th.start()
            print("解密完毕")
        else:
            pyperclip.copy(decode)
            print("解密完毕，粘贴查看")


def translate():
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.33)
    str = pyperclip.paste()
    print("获取到剪切板信息--uyume")
    print(str)
    encode(str)
    decode(str)


if __name__ == "__main__":
    print("加密通话0.01 by uyume")
    print("选中文本按住ctrl+shift+d，加密文本并粘贴或者解密")
    keyboard.add_hotkey('ctrl+shift+d', translate)
    keyboard.wait()
