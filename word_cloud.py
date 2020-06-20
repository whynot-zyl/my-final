import jieba# 导入词云制作库wordcloud和中文分词库jieba
import wordcloud
import numpy


def CreatWordcloud():
    # 构建并配置词云对象w，注意要加scale参数，提高清晰度
    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path='msyh.ttc',
                            scale=15)

    f = open('comments.txt',"r",encoding='utf-8').read()
    txtlist = jieba.lcut(f)
    string = " ".join(txtlist)
    # 将string变量传入w的generate()方法，给词云输入文字
    w.generate(string)

    # 将词云图片导出到当前文件夹
    w.to_file('wordcloud.png')
    f.close()

def display(): # 显示词云
    CreatWordcloud()
    import matplotlib.pyplot as plt  # plt 用于显示图片
    import matplotlib.image as mpimg  # mpimg 用于读取图片
    import numpy as np

    lena = mpimg.imread('DSC_0015.jpg')  # 读取和代码处于同一目录下的 lena.png
    # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
    lena.shape  # (512, 512, 3)
    plt.imshow(lena)  # 显示图片
    plt.axis('off')  # 不显示坐标轴
    plt.show()


