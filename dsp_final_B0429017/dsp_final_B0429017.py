'''
B0429017_資工二_陳蕾
訊號與系統、pygame期末Project <來抓我>
程式碼為自己打的 沒有參考資料
圖片皆來自 自己的相簿以及免費網站https://zh.icons8.com/
聲音皆來自 自己錄的=..=
'''
#--coding:utf-8--
import pygame, sys,time
from pygame.locals import *
from winsound import *
from random import *

#放大家的資料(照片,名字,音檔1.2.3)
person_info = [('17_resize_resize.PNG', 'Chen Lei', '17_1.WAV', '17_2.WAV','17_3.WAV'),
         ('30_resize_resize.PNG', 'Moon Dragon', '30_1.WAV', '30_2.WAV','30_3.WAV'),
         ('40_resize_resize.PNG', 'Cloud Cloud' , '40_1.WAV', '40_2.WAV','40_3.WAV'),
         ('43_resize_resize.PNG', 'Stop Fish' , '43_1.WAV', '43_2.WAV','43_3.WAV')]

#寫字(字串，字體，screen，位置x，位置y，顏色)
def printtxt(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
#更改背景音樂狀態
def set_bgsound():
    global bgsoundOn#如果原本為true則改為停止撥放並更改圖示
    if(bgsoundOn):
        screen.blit(no_sound,[15,10]) 
        PlaySound(None, SND_PURGE)#停止播放所有指定聲音
        bgsoundOn=False
    else:#如果是false改為開始撥放並更改圖示
        screen.blit(yes_sound,[15,10]) 
        PlaySound('bg.WAV', SND_FILENAME|SND_ASYNC|SND_LOOP)#後兩者(允許聲音異步播放/連續撥放)
        bgsoundOn=True
        
#背景音樂
def show_bgsound_pic():       
    global bgsoundOn
    if(bgsoundOn):#如果正在撥放則顯示撥放中圖片
        screen.blit(yes_sound,[15,10]) 
    else:#不是的話顯示停止音樂
        screen.blit(no_sound,[15,10]) 

#滑鼠
def draw_mouse_hand():
    x, y = pygame.mouse.get_pos()#獲得鼠标位置
    if(time.time()%1<0.5):#每0.5sec換圖片,因為我的滑鼠是會動的
        mouse_pic=mouse_pic1
    else:
        mouse_pic=mouse_pic2
    x-=mouse_pic.get_width() / 2
    y-=mouse_pic.get_height() / 2#計算圖的正中間
    screen.blit(mouse_pic, (x, y))
    pygame.display.update()

#等使用者按鍵
def waitForAnyKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:#當按下任何鍵則跳出迴圈
                return
    
#關卡 開門                
def open_door():
    for l in level1:
        if(l['i']<=event.pos[0]<=l['i']+100 and l['j']<=event.pos[1]<=l['j']+100):#看是在哪一個正方形
            if(l['i']==answeri and l['j']==answerj):#如果是正確答案的正方形
                screen.blit(pic[personChosen],[l['i'],l['j']])
                channel.set_volume(1)#最大音量1
                channel.play(sound[personChosen][1])#撥放聲音
                printtxt("you find "+person_info[personChosen][1]+" !!!", topicfont, screen, 300, 240,[255, 0, 0])
                printtxt("Press any key to next page", txtfont, screen,350, 300,[255, 0, 0])
                pygame.display.update()
                waitForAnyKey()#等待使用者按下按鍵
                global page
                page=False#跳至下一頁
            else:#不是正確答案的正方形
                l['color']=(255,255,255)#顏色改成白色
                distance=abs(l['i']-answeri)+abs(l['j']-answerj)
                vol=(10-distance*0.02)*0.1#計算距離來換算成音量大小
                if(vol<0):
                    vol=0
                if(vol==0):#離太遠放音樂2,並放最大聲
                    channel.set_volume(1)
                    channel.play(sound[personChosen][2])
                else:#不會的話放音樂0並按照距離設定音量
                    channel.set_volume(vol)
                    channel.play(sound[personChosen][0])
                pygame.display.update()
                #waitForAnyKey()

#往上飛
def fly(up):
    global playerj
    if(up):#如果要往上飛,人物縱座標往上
        playerj+=20
    else:#非則往下
        playerj-=20
                                
#initial
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 480), 0, 32)#創建窗口
pygame.display.set_caption("來抓我")#標題

#全域變數
personChosen=0#選定人物
bgsoundOn=True#背景音樂是否開啟

#圖片
mouse_img1='hand1.png'#滑鼠1
mouse_img2='hand2.png'#滑鼠2
yes_sound=pygame.image.load('yesSound_resize.png')#bgsound圖片(音量開啟)
no_sound=pygame.image.load('noSound_resize.png')#bgsound圖片(音量關閉)
start_img=pygame.image.load('start.PNG') #開始頁面的按鈕(開始)
exit_img=pygame.image.load('exit.PNG')#開始頁面的按鈕(離開)
gift_img=pygame.image.load('gift.png')#最後頁面的禮物

#滑鼠圖片轉換(convert_alpha()帶透明部分圖可用)
mouse_pic1=pygame.image.load(mouse_img1).convert_alpha()
mouse_pic2=pygame.image.load(mouse_img2).convert_alpha()

#字體大小與字型
topicfont=pygame.font.SysFont("Comic Sans MS", 30)
txtfont=pygame.font.SysFont("Comic Sans MS", 20)
littlefont=pygame.font.SysFont("Comic Sans MS", 10)

#放person照片的list
pic= []
#放person音樂的二維list
sound=[]
for rowCount in range(len(person_info)):
    sound.append([0]*3)#用append做成二維
    
for i in range(len(person_info)):
    pic.append(pygame.image.load(person_info[i][0]))#放入圖片檔
    for j in range(3):           
        sound[i][j]=(pygame.mixer.Sound(person_info[i][j+2]))#放入音樂檔
        
pygame.mouse.set_visible(False)#隱藏滑鼠
PlaySound('bg.WAV', SND_FILENAME|SND_ASYNC|SND_LOOP)#後兩者(允許聲音異步播放/連續撥放)

pygame.display.update()

#第一頁(開始頁)
page=True
while page:
    for event in pygame.event.get():#獲得事件
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==MOUSEBUTTONDOWN and 200<=event.pos[0]<=407 and 300<=event.pos[1]<=367: #離開按鈕
            pygame.quit()
            sys.exit()
        elif event.type==MOUSEBUTTONDOWN and 200<=event.pos[0]<=407 and 200<=event.pos[1]<=267: #start按鈕
            page=False
        elif event.type == KEYDOWN and event.key == ord('s'): #s控制bgsound
            set_bgsound()
    screen.fill([255,255,255])#背景白色
    printtxt("a game to catch us", topicfont, screen, 180, 100,[0, 200, 255])
    screen.blit(exit_img,[200,300])
    screen.blit(start_img,[200,200]) 
    show_bgsound_pic()#顯示背景音樂撥放狀態之圖片
    printtxt("press 's' to",littlefont,screen,13,35,[100,100,100])
    printtxt("stop the bgsound",littlefont,screen,5,48,[100,100,100]) 
    draw_mouse_hand()#畫出隱藏之鼠標現在位置
    pygame.display.update()
    
#頁面2
page=True        
while page:
    for event in pygame.event.get():#獲得事件
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == ord('s'):#按s可以關閉音樂或開啟音樂
            set_bgsound()
        #四個不同的人物位置
        elif event.type==MOUSEBUTTONDOWN and 150<=event.pos[0]<=250 and 120<=event.pos[1]<=220: 
            personChosen=0#人物編號
            page=False#前往下一頁
        elif event.type==MOUSEBUTTONDOWN and 350<=event.pos[0]<=450 and 120<=event.pos[1]<=220: 
            personChosen=2#人物編號
            page=False#前往下一頁
        elif event.type==MOUSEBUTTONDOWN and 150<=event.pos[0]<=250 and 300<=event.pos[1]<=400: 
            personChosen=1#人物編號
            page=False#前往下一頁
        elif event.type==MOUSEBUTTONDOWN and 350<=event.pos[0]<=450 and 300<=event.pos[1]<=400: 
            personChosen=3#人物編號
            page=False#前往下一頁
    screen.fill([255,255,255])#白色刷新
    printtxt("who do you want to catch", txtfont, screen, 180, 70,[50, 155, 155])
    show_bgsound_pic()
    #畫圖以及名字
    person=0;
    for i in range(150,550,200):
        for j in range(120,320,180):
            screen.blit(pic[person],[i,j])#顯示人物圖片
            printtxt(person_info[person][1], txtfont, screen, i, j+110,[100, 200, 255])#顯示人物名
            person=person+1 
    draw_mouse_hand()#畫出滑鼠
    pygame.display.update()  
    
#關卡解說
page=True
while page:
    for event in pygame.event.get():#獲得事件
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == ord('s'):
            set_bgsound()
        elif event.type == KEYDOWN:
            page=False#按任何鍵跳出
    screen.fill([0,0,0])#黑色填滿
    printtxt("you have chosen "+person_info[personChosen][1], topicfont, screen, 180, 70,[100, 100, 155])
    printtxt("now you have to find her", txtfont, screen, 150, 120,[100, 100, 155])
    printtxt("click on the squares to hear if you are close to her", txtfont, screen, 80, 150,[100, 100, 155])
    printtxt("press any key to start", topicfont, screen, 80, 250,[255, 50, 0])
    show_bgsound_pic()
    draw_mouse_hand()
    pygame.display.update()  

#放正方形的i,j,顏色
level1=[]
for i in range(20,540,100):#640*480
    for j in range(55,380,100):#畫出長方形的函式:Rect(left,top,width,height)
        newdoor = {'i': i,'j':j,'color':(randint(150,255),randint(150,255),randint(150,255)),}#隨機找顏色
        level1.append(newdoor)#新增一列
#隨機找一個放答案        
answeri=randrange(20,540,100)
answerj=randrange(55,380,100)
channel = pygame.mixer.find_channel() #找一個可以撥放的通道
channel.set_volume(1)#設定最大音量

#關卡
page=True
while page:    
    for event in pygame.event.get():#獲得事件
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == ord('s'):#按下s停止撥放背景音樂
            set_bgsound()
        elif event.type==MOUSEBUTTONDOWN and 20<=event.pos[0]<=620 and 55<=event.pos[1]<=455:#在正方形區塊
            open_door()
    screen.fill([255,255,255])#白色填滿
    printtxt("could have find "+person_info[personChosen][1], txtfont, screen, 200, 15,[128, 128, 255])
    for l in level1:#640*480
        pygame.draw.rect(screen, l['color'], (l['i'], l['j'], 100, 100))#畫出長方形的函式:Rect(left,top,width,height)
    show_bgsound_pic()#畫出背景音樂撥放狀態圖片
    draw_mouse_hand()#畫出鼠標
    pygame.display.update()  

#匯入pyaudio 以及numpy library
from pyaudio import PyAudio, paInt16 
import numpy as np 

NUM_SAMPLES = 2000#樣本數
SAMPLING_RATE = 8000#取樣頻率

# 開啟聲音的輸入
pa = PyAudio() 
stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, 
                frames_per_buffer=NUM_SAMPLES) 

flyUp=False
page=True
playeri=2
playerj=380
#結束頁面
while page:
    for event in pygame.event.get():#獲得事件
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == ord('s'):
            set_bgsound()
        elif event.type==KEYDOWN and event.key == ord('z'):#z可以往下飛  
            flyUp=True
        elif event.type==KEYUP and event.key == ord('z'):
            flyUp=False
    
    if(playeri>=530 and playerj<=5):#飛到禮物那裏了
        printtxt("Press any key to exit the game", txtfont, screen,350, 100,[250, 100, 200])
        pygame.display.update() 
        waitForAnyKey()
        page=False
        
    screen.fill([255,255,255])
    fly(flyUp)#往上飛還是往下飛
    audioData = stream.read(NUM_SAMPLES) #讀入麥克風數據
    audio_data = np.fromstring(audioData, dtype=np.short) #將讀入的數據轉為數據組
    if(np.max(abs(audio_data))>15000):#數據絕對值大於15000時代表有聲音輸入，則往右20
        playeri+=20
    else:
        playeri-=10#非則往左10
        
    if(playeri<0):#避免出邊界
        playeri=0
    elif (playeri>540):
        playeri=540
    if(playerj<0):
        playerj=0
    elif (playerj>380):
        playerj=380
        
    printtxt("Thank you for playing this game", topicfont, screen, 70, 200,[128, 128, 255])
    printtxt("I'm glad that you like it :)", topicfont, screen, 100, 260,[143, 206, 200])
    #將左下角以外的地方畫上長方形遮蔽
    pygame.draw.rect(screen, (128, 128, 255), (0, 0, playeri, playerj))
    pygame.draw.rect(screen, (128, 128, 255), (playeri, 0, 1000,playerj))
    pygame.draw.rect(screen, (128, 128, 255), (playeri, playerj,1000,1000))    
    printtxt("you win this game, shout to let us know you are happy :)", txtfont, screen, 80, 400,[245, 200, 125])
    screen.blit(pic[personChosen],[playeri,playerj])#人物圖片顯示
    screen.blit(gift_img,[580,5])#禮物圖片顯示
    show_bgsound_pic()#背景音樂圖片
    pygame.display.update() 
                 
            
