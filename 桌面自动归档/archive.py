import json
import os
import re
import shutil
import sys
import uuid
import winreg
from datetime import datetime

CONFIG = {
    "EN_TIME_CLASS": 1,
    "EN_DIR_CLASS": 0,
    "CLASS_DIR": "",
    "FILE_CLASS_TYPE": "(?=^.*[^\\.lnk]$)(?=[^desktop.ini])",
    "FILE_CLASS": {},
    "DIR_CLASS_TYPE": "\\.*",
    "DIR_CLASS": {}
}


def fitterDir(dirs, desktopPath):
    classDir = CONFIG['CLASS_DIR']
    needDirs = []
    if not classDir:  # 如果归档路径就为桌面
        needInDesktop(needDirs, dirs)
    else:
        if not os.path.isabs(classDir):  # 绝对路径
            classDir = os.path.join(desktopPath, classDir)
        absNeedInDesktop(classDir, desktopPath, needDirs, dirs)
    return needDirs


def absNeedInDesktop(classDir, desktopPath, needDirs, dirs):
    if classDir.startswith(desktopPath):  # 在桌面下
        if classDir == desktopPath:
            needInDesktop(needDirs, dirs)
        else:
            classDir = classDir.replace(desktopPath + os.sep, '')
            for name in dirs:
                pathName = name + os.sep if os.sep in classDir else name
                if not classDir.startswith(pathName):
                    needDirs.append(name)
    else:
        needDirs.extend(dirs)

def needInDesktop(needDirs, dirs):
    if CONFIG['EN_TIME_CLASS']:  # 按时间归档的不动时间归档
        for name in dirs:
            if not re.match('^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2]\d|3[0-1])', name):
                needDirs.append(name)
    else:  # 不按时间归档不动归档规则目录
        for name in dirs:
            for dirName in {**CONFIG['FILE_CLASS'], **CONFIG['DIR_CLASS']}.keys():
                pathName = name + os.sep if os.sep in dirName else name
                if not dirName.startswith(pathName):
                    needDirs.append(name)


def readFiles():  # 读取桌面所有的文件路径和名称储存起来
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    desktopPath = winreg.QueryValueEx(key, "Desktop")[0]
    vals = os.listdir(desktopPath)
    files = []
    dirs = []
    for file in vals:
        filePath = os.path.join(desktopPath, file)
        if os.path.isfile(filePath) and re.match(CONFIG['FILE_CLASS_TYPE'], file):
            files.append(file)
        elif os.path.isdir(filePath) and re.match(CONFIG['DIR_CLASS_TYPE'], file):
            dirs.append(file)
    return desktopPath, files, fitterDir(dirs, desktopPath)


def classifyFiles(path):  # 把文件分类
    with open(path, 'r', encoding='utf8') as fp:
        jData = json.load(fp)
        global CONFIG
        CONFIG = {**CONFIG, **jData}
        CONFIG['CLASS_DIR'] = CONFIG['CLASS_DIR'].strip()


def createAndMv(targetInfo):
    print('开始归档...')
    source = targetInfo['source']
    target = targetInfo['target']
    isTime = targetInfo['isTime']
    dirInfo = targetInfo['dirInfo']
    fileInfo = targetInfo['fileInfo']
    createDir(target)
    if isTime:
        target = createDirByTime(target)
    mvFiles(source, target, fileInfo)
    mvDirs(source, target, dirInfo)
    return


def createDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def mvFiles(source, target, files):  # 移动文件到相应的路径
    for key in files.keys():
        dirPath = os.path.join(target, key) if key else target
        print('正在归档文件至', key, '，路径为', dirPath)
        if key is not None:
            createDir(dirPath)
        for file in files[key]:
            print('归档文件', file)
            filePath = rename(source, dirPath, file, 1)
            shutil.move(filePath, dirPath)


def mvDirs(source, target, dirs):  # 移动文件到相应的路径
    for key in dirs.keys():
        targetPath = os.path.join(target, key) if key else target
        print('正在归档文件夹至', key, '，路径为', targetPath)
        if key is not None:
            createDir(targetPath)
        for dir in dirs[key]:
            print('归档文件夹', dir)
            dirPath = rename(source, targetPath, dir, 0)
            shutil.move(dirPath, targetPath)


def rename(source, target, name, isFile):
    sourcePath = os.path.join(source, name)
    targetPath = os.path.join(target, name)
    renamePath = sourcePath
    if os.path.exists(targetPath):
        if isFile:
            dFile = os.path.splitext(name)
            dName = dFile[0]
            dType = dFile[1]
            renName = dName + str(uuid.uuid1()).replace('-', '') + dType
            renamePath = os.path.join(source, renName)
            print('目标文件重复，', name, '重命名为', renName)
        else:
            renName = name + str(uuid.uuid1()).replace('-', '')
            renamePath = os.path.join(source, renName)
            print('目标文件夹重复，', name, '重命名为', renName)
        os.rename(sourcePath, renamePath)
    return renamePath


def createDirByTime(target):
    dirName = datetime.now().strftime('%Y-%m-%d')
    dirPath = os.path.join(target, dirName)
    print('首先按时间归档，当前归档为', dirName, '，归档路径为', dirPath)
    createDir(dirPath)
    return dirPath


def generateTargetInfo(fileInfo):
    print('开始生成整理信息...')
    targetInfo = {
        'isTime': CONFIG['EN_TIME_CLASS'],
        'source': fileInfo[0],
        'target': CONFIG['CLASS_DIR'] if CONFIG['CLASS_DIR'].strip() else fileInfo[0],
        'fileInfo': {},
        'dirInfo': {}
    }
    if CONFIG['EN_DIR_CLASS']:
        print('整理文件夹信息...')
        setDirInfo(fileInfo[2], targetInfo['dirInfo'], 'DIR_CLASS')
    print('整理文件信息...')
    setDirInfo(fileInfo[1], targetInfo['fileInfo'], 'FILE_CLASS')
    return targetInfo


def setDirInfo(names, dirInfo, CLASS):
    for name in names:
        dir = getDirName(name, CLASS)
        if dir not in dirInfo:
            dirItem = []
            dirItem.append(name)
            dirInfo[dir] = dirItem
        else:
            dirInfo[dir].append(name)

def getDirName(name, CLASS):
    for dir in CONFIG[CLASS].keys():
        if re.match(CONFIG[CLASS][dir], name):
            return dir
    return None


if __name__ == "__main__":
    print('开始进行桌面自动归档（作者：uyume 版本：0.0.1）...')
    classifyFiles(os.path.join(os.path.dirname(sys.argv[0]), "config.json"))
    print('配置加载信息为：', CONFIG)
    fileInfo = readFiles()
    print('读取桌面欲整理信息为：', fileInfo)
    targetInfo = generateTargetInfo(fileInfo)
    print('整理信息生成为', targetInfo)
    createAndMv(targetInfo)
    print('归档结束!')
