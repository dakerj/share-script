# 自动归档脚本使用说明
uyume@qq:2463705649
## 默认参数
```json
{
    // 是否按时间归档
    "EN_TIME_CLASS": 1, 
    // 是否归档文件夹
    "EN_DIR_CLASS": 0, 
    // 归档目标路径
    "CLASS_DIR": "", 
    // 需归档文件正则，归档除了快捷方式和桌面ini外的所有文件
    "FILE_CLASS_TYPE": "(?=^.*[^\\.lnk]$)(?=[^desktop.ini])",
    // 文件归档分类正则
    "FILE_CLASS": {}, 
    // 需归档文件夹正则，归档所有文件夹
    "DIR_CLASS_TYPE": "\\.*", 
    // 文件夹归档分类正则
    "DIR_CLASS": {} 
}
```
## EN_TIME_CLASS参数
为1时在归档路径下首先按时间归档，归档文件夹名为**年年年年-月月-日日** 
## EN_DIR_CLASS参数
为1时，如果归档路径在桌面会归档除脚本创建归档文件夹外的文件夹，如果归档路径不在桌面则归档所有文件夹
## CLASS_DIR参数
桌面的文件和文件夹会按照规则归档到该路径下
## FILE_CLASS_TYPE
桌面上那些文件需要归档，用正则表达式表示
## FILE_CLASS
文件归档规则，按照正则的规则归档
例如配置：
```json
"FILE_CLASS": {
  "word": ".*\\.docx|.*\\.doc",
  "office\\excel": ".*\\.xlsx|.*\\.xls"
}
```
配置会将后缀为doc和docx的word文档归档到**$CLASS_DIR\word或$CLASS_DIR\年年年年-月月-日日\word**
,后缀为xlsx和xls的excel文档归档到**$CLASS_DIR\office\excel或$CLASS_DIR\年年年年-月月-日日\office\excel**。

如果同一文件满足两个规则，优先第一个匹配到的规则。

**如果没匹配到任何规则，则直接移到归档目录下**

如果归档时存在同名文件会重命名文件。
## DIR_CLASS_TYPE 和 DIR_CLASS 参数
同FILE_CLASS_TYPE和FILE_CLASS参数