echo 开始下载模块
Install-Module DirColors -Scope CurrentUser
Install-Module posh-git -Scope CurrentUser
Install-Module oh-my-posh -Scope CurrentUser
echo 开始创建配置ps配置文件
if (!(Test-Path -Path $PROFILE)) {
  New-Item -ItemType File -Path $PROFILE -Force
}
Set-Content -Path $PROFILE -Value "chcp 65001`nImport-Module DirColors`nImport-Module posh-git`nImport-Module oh-my-posh`nSet-PoshPrompt Robby`n" 
echo 开始下载window缺乏字体
curl -Uri  https://hub.fastgit.xyz/ryanoasis/nerd-fonts/releases/download/v2.1.0/Hack.zip -OutFile ./Hack.zip
echo 脚本结束，请自行设置终端字体
pause