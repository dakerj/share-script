downloadTool=''
shellUrl='https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh'
replaceUrl='https://raw.fastgit.org/ohmyzsh/ohmyzsh/master/tools/install.sh'
replace='0'
github="github.com"
setDownloadTool(){
	if ! command -v wget; then
		if ! command -v curl; then
			echo 'curl/wget 未安装, 将自动安装wget'
			apt install wget
			downloadTool=wget
		else
			downloadTool=curl
		fi
	else
		downloadTool=wget
	fi
}
setReplace(){
	read -r -p "是否替换为镜像源？[y/n]" is
	case $is in
		[yY][eE][sS]|[yY])
			replace=1
			;;

		*)
	esac
}
installIfNot(){
	if ! command -v $1; then
		echo $1'未安装, 将自动安装'$1
		apt install $1
	fi
}
cloneIfNot(){
	if [ ! -e "./$1/$1.zsh" ]; then
		rm -rf $1
		echo "开始下载$2"
		git clone https://$github/zsh-users/$1.git
	fi
	isDownloadOk "./$1/$1.zsh" $2
}
cdTempDir(){
	if [ ! -d $1 ]; then
		mkdir $1
	fi
	cd $1
}
downloadInstallShell(){
	if [ ! -e "install.sh" ]; then
		echo 'downloadTool=$downloadTool'
		if [ "$replace" = "1" ]; then
				echo '替换oh-my-zsh安装脚本下载为镜像源'
				shellUrl=$replaceUrl
		fi
		if [ "$downloadTool" != "" ]; then
			$downloadTool $shellUrl
		else
			echo 'curl/wget 未安装，退出脚本'
			exit 1
		fi
	fi
}
isDownloadOk(){
	if [ ! -e $1 ]; then
		echo $2'下载失败'
		if [ x$3 != x ]; then
			exit 1
		fi
		else
		echo $2'下载成功'
	fi
}
shInstall(){
	if [ "$replace" = "1" ]; then
		echo '替换oh-my-zsh安装脚本为镜像源'
		sed -i 's/github.com/hub.fastgit.xyz/g' ./install.sh
	fi
	sh ./install.sh
	if [ -d "~/.oh-my-zsh" ]; then
		cd ..
		rm -rf ./tempdir
	fi
}
installPlugins(){
	if [ -d "~/.oh-my-zsh" ]; then
		cd ..
		rm -rf ./tempdir
	fi
	echo '开始下载安装插件'
	sed -i 's/^plugins=(.*)$/plugins=(sudo z zsh-autosuggestions zsh-syntax-highlighting git)/g' ~/.zshrc
	cd ~/.oh-my-zsh/custom/plugins/
	if [ "$replace" = "1" ]; then
		github="hub.fastgit.xyz"
	fi
	cloneIfNot zsh-syntax-highlighting '语法高亮插件'
	#sed -i 's/^source ~\/.oh-my-zsh\/custom\/plugins\/zsh-syntax-highlighting\/zsh-syntax-highlighting.zsh$//g' ~/.zshrc
	#echo "source ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >>~/.zshrc
	cloneIfNot zsh-autosuggestions '语法补全插件'
	#sed -i 's/^source ~\/.oh-my-zsh\/custom\/plugins\/zsh-autosuggestions\/zsh-autosuggestions.zsh$//g' ~/.zshrc
	#echo "source ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh" >>~/.zshrc
}
installOhMyZsh(){
	isInstall=1
	if [ -d ~/.oh-my-zsh ]; then
		read -r -p "检测到oh-my-zsh可能已经装好，是否继续运行oh-my-zsh安装脚本？[y/n]" iss
		case $iss in
			[nN])
				isInstall=0
				;;
			*)
		esac
			
	fi
	if [ "$isInstall" = "1" ]; then
		cdTempDir tempdir
		downloadInstallShell
		isDownloadOk install.sh 'oh-my-zsh安装脚本' 1
		shInstall
	fi
}
installIfNot zsh
installIfNot git
setDownloadTool
setReplace
installOhMyZsh
installPlugins

tail ~/.zshrc
#source ~/.zshrc