echo 'change pip source start'
if (!(Test-Path -Path $HOME/pip)) {
  New-Item -ItemType Directory -Path $HOME/pip -Force
}

if (!(Test-Path -Path $HOME/pip/pip.ini)) {
    New-Item -ItemType File -Path $HOME/pip/pip.ini -Force
}

Set-Content -Path $HOME/pip/pip.ini -Value "[global]`nindex-url = https://mirrors.aliyun.com/pypi/simple`n[install]`ntrusted-host = mirrors.aliyun.com`n"
echo 'change pip source end'
pause