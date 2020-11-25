# ltr
ltr是一种新型的键盘布局,是根据的workman,programmer-dvorak得到的灵感,充分吸收了workman的人体工程学原理,和programmer-dvorak的符号优化.
同时,ltr在保证英文高效输入的前提下设计了汉语拼音专属的双拼方案.(这里只提供linux的实现方案,windows可以修改注册表和编写autohotkey脚本语言实现)
## 布局预览
![ltr预览](./ltr.png)
## 实现键位布局
1. 复制99-ltr.hwdb到/etc/udev/hwdb.d
2. $ sudo udevadm hwdb --update
3. $ sudo udevadm trigger
## 实现热键功能
1. 确保已经安装好python3(python --version)
2. 复制hotkey.py和hotkey.service到~/.config/systemd/user/下(如果没有这个文件夹需要创建)
3. chmod +x hotkey.py
4. systemctl --user enable hotkey.service
5. systemctl --user start hotkey.service
## 实现双拼功能
1. 确保安装fcitx5,[archwiki](https://wiki.archlinux.org/index.php/Fcitx5)有详细的教程
2. $ sudo pacman -U libime-0.0.0.20201013-1-x86_64.pkg.tar.zst (这是archlinux的包管理器安装,可以改为自己用的包管理器)
3. killall fcitx5 
4. fcitx5 &
