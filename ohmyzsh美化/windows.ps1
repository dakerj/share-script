echo ��ʼ����ģ��
Install-Module DirColors -Scope CurrentUser
Install-Module posh-git -Scope CurrentUser
Install-Module oh-my-posh -Scope CurrentUser
echo ��ʼ��������ps�����ļ�
if (!(Test-Path -Path $PROFILE)) {
  New-Item -ItemType File -Path $PROFILE -Force
}
Set-Content -Path $PROFILE -Value "chcp 65001`nImport-Module DirColors`nImport-Module posh-git`nImport-Module oh-my-posh`nSet-PoshPrompt Robby`n" 
echo ��ʼ����windowȱ������
curl -Uri  https://hub.fastgit.xyz/ryanoasis/nerd-fonts/releases/download/v2.1.0/Hack.zip -OutFile ./Hack.zip
echo �ű������������������ն�����
pause