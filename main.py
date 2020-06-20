from tkinter import *   # 导入tkinter库
import get_data
import nlp
import word_cloud
import time
import condition

#判断是否提示loding
flag=0
#爬取函数
def GetComment():
    submit.config(text="正在爬取请稍等。。。")
    global flag
    flag=1
#显示功能菜单
def NextMenu():
    print(2)
    submit.forget()
    cloud.place(relx=0.30, y=50)
    nlp.place(relx=0.30, y=125)
    comdition.place(relx=0.30, y=200)


if __name__ == '__main__':
    root = Tk()
    def task(): # 实现输出正在加载字样
        print(flag)
        global root
        # 代码
        root.after(1000, task)  # 1000是循环间隔，单位毫秒
        if(flag==1):
            get_data.get()
            NextMenu()
    task()
    root.title('疫情分析')
    root.geometry('400x400')
    submit = Button(root, command=GetComment,text='获取数据', bg='#d3fbfb', fg='red', width=20, height=2, relief=RIDGE)
    submit.place(relx=0.30, y=200)
    cloud = Button(root, command=word_cloud.display, text='评论的词云', bg='#d3fbfb', fg='red', width=20, height=2, relief=RIDGE)
    nlp = Button(root, command=nlp.anlyse, text='网民情绪统计', bg='#d3fbfb', fg='red', width=20, height=2,relief=RIDGE)
    comdition = Button(root, command=condition.display, text='实时疫情', bg='#d3fbfb', fg='red', width=20, height=2, relief=RIDGE)
    # 进入消息循环


    root.mainloop()