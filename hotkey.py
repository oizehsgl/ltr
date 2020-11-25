#!/urs/bin/python3
#import subprocess
import evdev
import os
from evdev import UInput,ecodes
#获取键盘设备
#device=evdev.InputDevice('/dev/input/by-id/usb-SINO_WEALTH_Keyboard-event-kbd')
device=evdev.InputDevice('/dev/input/by-id/usb-04f3_0103-event-if00')
#device=evdev.InputDevice('/dev/input/by-path/platform-i8042-serio-0-event')
#设备独占资源
device.grab()
#获取输入对象
uinput=UInput()
#存储事件状态
es=0
#存储按键值,
kc=0
#存储按键状态
ks=0
#存储前一个按键值
pkc=0
#存储前一个按键状态
pks=0
#存储修饰键状态
mod=0
pmod=0
############################################################
#
#   快捷键辅助恢复
#
############################################################



################################
#
#   基础函数与字典
#
################################

#键值字典
key_code_dict={'esc': 1, 'f1': 59, 'f2': 60, 'f3': 61, 'f4': 62, 'f5': 63, 'f6': 64, 'f7': 65, 'f8': 66, 'f9': 67, 'f10': 68, 'f11': 87, 'f12': 88, 'sysrq': 99, 'scrolllock': 70, 'pause':119, 'leftshift': 42, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, 'leftbrace': 26, 'rightbrace': 27, '6': 7, '7': 8, '8': 9, '9': 10, '0': 11, 'rightshift': 54, 'insert': 110, 'home': 102, 'pageup': 104, 'numlock': 69, 'kpslash': 98, 'kpasterisk': 55, 'kpminus': 74, 'backspace': 14, 'apostrophe': 40, 'f': 33, 'u': 22, 'z': 44, 'comma': 51, 'grave': 41, 'dot': 52, 'v': 47, 'd': 32, 'c': 46, 'semicolon': 39, 'slash': 53, 'backslash': 43, 'delete': 111, 'end': 107, 'pagedown': 109, 'kp7': 71, 'kp8': 72, 'kp9': 73, 'kpplus': 78, 'capslock': 58, 'o': 24, 'a': 30, 'e': 18, 'i': 23, 'g': 34, 'minus': 12, 'l': 38, 'n': 49, 't': 20, 'r': 19, 's': 31, 'p': 25, 'kp4': 75, 'kp5': 76, 'kp6':77, 'tab': 15, 'x': 45, 'q': 16, 'j': 36, 'y': 21, 'k': 37, 'equal': 13, 'h': 35, 'm': 50, 'w': 17, 'b': 48, 'enter': 28, 'up': 103, 'kp1': 79, 'kp2': 80, 'kp3': 81, 'kpenter': 96, 'leftctrl':29, 'leftmeta': 125, 'leftalt': 56, 'space': 57, 'rightctrl': 97, 'compose': 127, 'rightalt': 100, 'left': 105, 'down': 108, 'right': 106, 'kp0': 82, 'kpdot': 83,'rightmeta': 126}

#值键字典
code_key_dict={1: 'esc', 59: 'f1', 60: 'f2', 61: 'f3', 62: 'f4', 63: 'f5', 64: 'f6', 65: 'f7', 66: 'f8', 67: 'f9', 68: 'f10', 87: 'f11', 88: 'f12', 99: 'sysrq', 70: 'scrolllock', 191: 'pause', 42: 'leftshift', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 26: 'leftbrace', 27: 'rightbrace', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0', 54: 'rightshift', 110: 'insert', 102: 'home', 104: 'pageup', 69: 'numlock', 98: 'kpslash', 55: 'kpasterisk', 74: 'kpminus', 14: 'backspace', 40: 'apostrophe', 33: 'f', 22: 'u', 44: 'z', 51: 'comma', 41: 'grave', 52: 'dot', 47: 'v', 32: 'd', 46: 'c', 39: 'semicolon', 53: 'slash', 43: 'backslash', 111: 'delete', 107: 'end', 109: 'pagedown', 71: 'kp7', 72: 'kp8', 73: 'kp9', 78: 'kpplus', 58: 'capslock', 24: 'o', 30: 'a', 18: 'e', 23: 'i', 34: 'g', 12: 'minus', 38: 'l', 49: 'n', 20: 't', 19: 'r', 31: 's', 25: 'p', 75: 'kp4', 76: 'kp5', 77: 'kp6', 15: 'tab', 45: 'x', 16: 'q', 36: 'j', 21: 'y', 37: 'k', 13: 'equal', 35: 'h', 50: 'm', 17: 'w', 48: 'b', 28: 'enter', 103: 'up', 79: 'kp1', 80: 'kp2', 81: 'kp3', 96: 'kpenter', 92: 'leftctrl', 125: 'leftmeta', 56: 'leftalt', 57: 'space', 97: 'rightctrl', 127: 'compose', 100: 'rightalt', 105: 'left', 108: 'down', 106: 'right', 82: 'kp0',  83: 'kpdot',126: 'rightmeta'}

#字符字典
char_code_dict={'!': -2,'1': 2, '@': -3, '2': 3, '#': -4, '3': 4, '$': -5, '4': 5, '%': -6, '5': 6, '{': -26, '[': 26, '}': -27, ']': 27, '^': -7, '6': 7, '&': -8, '7': 8, '*': -9, '8': 9, '(': -10, '9': 10, ')': -11, '0': 11, '\b': 74, '"': -40, '\'': 40, 'f': 33, 'u': 22, 'z': 44, '<': -51, ',': 51, '~': -41, '`': 41, '>': -52, '.': 52, 'v': 47, 'd': 32, 'c': 46, ':': -39, ';': 39, '?': -53, '/': 53, '|': -43, '\\': 43, '\t': 15, '\n': 28, 'o': 24, 'a': 30, 'e': 18, 'i': 23, 'g': 34, '_': -12, '-': 12, 'l': 38, 'n': 49, 't': 20, 'r': 19, 's': 31, 'p': 25, 'x': 45, 'q': 16, 'j': 36, 'y': 21, 'k': 37, '+': -13, '=': 13, 'h': 35, 'm': 50, 'w': 17, 'b': 48, ' ': 57, 'F': -33, 'U': -22, 'Z': -44, 'V': -47, 'D': -32, 'C': -46, 'O': -24, 'A': -30, 'E': -18, 'I': -23, 'G': -34, 'L': -38, 'N': -49, 'T': -20, 'R': -19, 'S': -31, 'P': -25, 'X': -45, 'Q': -16, 'J': -36, 'Y': -21, 'K': -37, 'H': -35, 'M': -50, 'W': -17, 'B': -48}

#down函数表示按键按下
def d(kc):
    uinput.write(ecodes.EV_MSC, ecodes.MSC_SCAN, kc)
    uinput.write(ecodes.EV_KEY, kc, 1)
    uinput.syn()
    return
#up函数表示按键弹起
def u(kc):
    uinput.write(ecodes.EV_MSC, ecodes.MSC_SCAN, kc)
    uinput.write(ecodes.EV_KEY, kc, 0)
    uinput.syn()
    return
#click函数表示点击键
def c(kc):
    d(kc)
    u(kc)
    return

################################
#
#   命令行
#
################################

#调用sxhkd执行命令行任务
def centre(kc):
   # d(key_code_dict['rightshift'])
    d(key_code_dict['rightctrl'])
    d(key_code_dict['rightalt'])
    d(key_code_dict['rightmeta'])
    c(kc)
    u(key_code_dict['rightmeta'])
    u(key_code_dict['rightalt'])
    u(key_code_dict['rightctrl'])
   # u(key_code_dict['rightshift'])
    return

def shift(kc):
    d(key_code_dict['leftshift'])
    c(kc)
    u(key_code_dict['leftshift'])
    return


def ctrl(kc):
    d(key_code_dict['rightctrl'])
    c(kc)
    u(key_code_dict['rightctrl'])
    return

def alt(kc):
    d(key_code_dict['rightalt'])
    c(kc)
    u(key_code_dict['rightalt'])
    return

def alt_cursor(kc):
    d(key_code_dict['rightalt'])
    cursor(kc)
    u(key_code_dict['rightalt'])
    return

def alt_char(kc):
    d(key_code_dict['rightalt'])
    char(kc)
    u(key_code_dict['rightalt'])
    return

def ctrl_cursor(kc):
    d(key_code_dict['rightctrl'])
    cursor(kc)
    u(key_code_dict['rightctrl'])
    return

def ctrl_char(kc):
    d(key_code_dict['rightctrl'])
    char(kc)
    u(key_code_dict['rightctrl'])
    return

def ctrl_shift(kc):
    d(key_code_dict['rightctrl'])
    shift(kc)
    u(key_code_dict['rightctrl'])
    return


def meta(kc):
    d(key_code_dict['rightmeta'])
    c(kc)
    u(key_code_dict['rightmeta'])
    return
def shift_centre(kc):
    d(key_code_dict['rightshift'])
    d(key_code_dict['rightctrl'])
    d(key_code_dict['rightalt'])
    d(key_code_dict['rightmeta'])
    c(kc)
    u(key_code_dict['rightmeta'])
    u(key_code_dict['rightalt'])
    u(key_code_dict['rightctrl'])
    u(key_code_dict['rightshift'])
    return

#命令行字典
command_dict={'semicolon': '', 'apostrophe': '', 'f': '', 'u': '', 'z': '', 'comma': '', 'dot': '', 'v': '', 'd': '', 'c': '', 'slash': '', 'backslash': '','backspace': '', 'o': 'oizehsgl', 'a': '', 'e': '', 'i': 'O_Nm1234', 'g': 'oizehsgl@gmail.com', 'l': '', 'n': 'O_Nm15129', 't': '', 'r': '', 's': '', 'delete': '','tab': '', 'x': '', 'q': '3057157713', 'j': '', 'y': '', 'k': '', 'h': '', 'm': 'O_Nm1860867', 'w': 'urxvt', 'b': 'bspc node -f @brother', 'p': "17805426480", 'enter': ''}
#使用subprocess调用命令行，有问题，无法像sxhkd一样，这里启动的都是子进程，一但把这个进程杀死就会关闭所有子进程，危险，尽量调用sxhkd
#def command(kc):
#    subprocess.Popen('su oizehsgl -c'+command_dict[code_key_dict[kc]], shell=True,cwd='/home/oizehsgl/')
#    return

################################
#
#   热字符串
#
################################

#热字符串定义
compose_dict={'semicolon': '', 'apostrophe': '', 'f': '', 'u': '', 'z': '', 'comma': '', 'dot': '', 'v': '', 'd': '', 'c': '', 'slash': '', 'backslash': '','backspace': '', 'o': '', 'a': '', 'e': '', 'i': '', 'g': '', 'l': '', 'n': '', 't': '', 'r': '', 's': '', 'delete': '','tab': '', 'x': '', 'q': '', 'j': '', 'y': '', 'k': '', 'hello world!': '', 'm': '', 'w': '', 'b': '', 'p': "", 'enter': ''}

def compose(kc):
    if compose_dict.__contains__(code_key_dict[kc]):
        for i in compose_dict[code_key_dict[kc]]:
            if char_code_dict[i]>=0:
                c(char_code_dict[i])
            else:
                d(key_code_dict['rightshift'])
                c(-char_code_dict[i])
                u(key_code_dict['rightshift'])
    return
################################
#
#   光标移动
#
################################

cursor_dict={'semicolon': ('semicolon',), 'apostrophe': ('apostrophe',), 'f': ('rightshift','pageup'), 'u': ('rightalt','up'), 'z': ('rightshift','pagedown'), 'comma': ('comma',), 'dot': ('dot',), 'v': ('pageup',), 'd': ('up',), 'c': ('pagedown',), 'slash': ('slash',), 'backslash': ('backslash',),'backspace': ('backspace',), 'o': ('rightshift','home'), 'a': ('rightalt','left'), 'e': ('rightalt','down'), 'i': ('rightalt','right'), 'g': ('rightshift','end'), 'l': ('home',), 'n': ('left',), 't': ('down',), 'r': ('right',), 's': ('end',), 'delete': ('delete',),'tab': ('tab',), 'x': ('x',), 'q': ('q',), 'j': ('j',), 'y': ('y',), 'k': ('k',), 'h': ('h',), 'm': ('m',), 'w': ('w',), 'b': ('b',), 'p': ('p',), 'enter': (0,'end','enter')}

def cursor(kc):
    if cursor_dict.__contains__(code_key_dict[kc]):
        if cursor_dict[code_key_dict[kc]][0]==0:
            for i in cursor_dict[code_key_dict[kc]][1:]:
                d(key_code_dict[i])
                u(key_code_dict[i])
        else:
            for i in cursor_dict[code_key_dict[kc]]:
                d(key_code_dict[i])
            for i in reversed(cursor_dict[code_key_dict[kc]]):
                u(key_code_dict[i])
    return

################################
#
#   符号映射
#
################################

#符号字典
char_dict={'semicolon':'@', 'apostrophe':'"', 'f':'#', 'u':'(', 'z':'[', 'comma':'{', 'dot':'}', 'v':']', 'd':')', 'c':':', 'backslash':'`', 'slash':'?','tab':'^', 'o':'|', 'a':'<', 'e':'*', 'i':'+', 'g':'%', 'l':'=', 'n':'-', 't':'/', 'r':'>', 's':'&', 'enter':'$','backspace':'~', 'x':'9', 'q':'7', 'j':'5', 'y':'3', 'k':'1', 'h':'0', 'm':'2', 'w':'4', 'b':'6', 'p':'8', 'delete': '!','space': '_'}

def char(kc):
    #这个判断不是必须的,以后可以去掉，包含所有键盘的字符
    if char_dict.__contains__(code_key_dict[kc]):
        if char_code_dict[char_dict[code_key_dict[kc]]]>0:
            c(char_code_dict[char_dict[code_key_dict[kc]]])
        else:
            d(key_code_dict['rightshift'])
            c(-char_code_dict[char_dict[code_key_dict[kc]]])
            u(key_code_dict['rightshift'])
    return

#修饰键字典

#                insert               capslock              numlock              leftshift               esc
mod_dict={key_code_dict['capslock']:512,key_code_dict['leftmeta']:128,key_code_dict['leftalt']:32,key_code_dict['leftctrl']:8,key_code_dict['leftshift']:2,key_code_dict['rightshift']:1,key_code_dict['rightctrl']:4,key_code_dict['rightalt']:16,key_code_dict['rightmeta']:64,key_code_dict['numlock']:256}


mod_click_dict={key_code_dict['capslock']:('capslock',),key_code_dict['leftmeta']:('leftmeta',),key_code_dict['leftalt']:('leftalt',),key_code_dict['leftctrl']:('esc',),key_code_dict['leftshift']:('leftshift',),key_code_dict['rightshift']:('rightshift',),key_code_dict['rightctrl']:('rightctrl',),key_code_dict['rightalt']:('rightalt',),key_code_dict['rightmeta']:('rightmeta',),key_code_dict['numlock']:('numlock',)}


def mod_click(kc):
    if mod_click_dict.__contains__(kc):
        for i in mod_click_dict[kc]:
            d(key_code_dict[i])
        for i in reversed(mod_click_dict[kc]):
            u(key_code_dict[i])
    return


#触发事件字典
event_dict={2:char,
           8:cursor,
           32:centre,
           128:compose,
           1:shift,
           33:shift_centre,
           4:ctrl,
           5:ctrl_shift,
           6:ctrl_char,
           12:ctrl_cursor,
           16:alt,
           24:alt_cursor,
           18:alt_char,
           64:meta}

################################
#
#   无限循环处理键盘输入
#
################################

for event in device.read_loop():
    #利用位移运算判断事件状态
    es=1>>es
    #如果是开始事件就把es设置为零
    if event.type==ecodes.EV_MSC:
         es=0
    #不是开始事件就利用es判断是否要输出事件
    else:
        #es为1证明一个击键未结束（击键分为三种abc，每种又有三个或两个事件012，a按下（0开始ev-msc，1按键ev-key，2结束syn），保持（1ev-key，2syn），。。。，弹起（0ev-msc，1ev-key，2syn））并且是ev-key状态，需要记录键码code，和键态value
        if es==1:
            pkc=kc
            pks=ks
            kc=event.code
            ks=event.value
        #es不为1，而且不是ev-msc，就证明是syn，此时一个击键结束，需要输出
        else:
            #先判断是不是修饰键
            if mod_dict.__contains__(kc):
                if ks!=2:
                    mod=((1023-mod_dict[kc])&mod)+ks*mod_dict[kc]
                if pkc==kc and pks==1 and ks==0:
                    mod_click(kc)
                    mod=0
            else:
                if event_dict.__contains__(mod):
                    if ks!=0:
                        event_dict[mod](kc)
                else:
                    if ks!=2:
                        uinput.write(ecodes.EV_MSC, ecodes.MSC_SCAN, kc) 
                    uinput.write(ecodes.EV_KEY, kc, ks) 
                    uinput.syn()      
#设备释放资源
device.ungrab()
uinput.close()
device.close()
