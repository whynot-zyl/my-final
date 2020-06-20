import requests
import json
import csv
import os
import get_data

def draw():
    get_data.GetCondition()
    result = {'province': [], 'province_confirmedCount': []}
    result['province'].append('台湾')
    result['province_confirmedCount'].append(18)
    result['province'].append('香港')
    result['province_confirmedCount'].append(56)
    result['province'].append('澳门')
    result['province_confirmedCount'].append(10)

    # 批量删除多余字符的函数
    def replace_something(source_str, replace_list):
        for line in replace_list:
            source_str = source_str.replace(line, "")
        return source_str

    with open("virus.csv", 'r', encoding='UTF-8') as csvFile:
        reader = csv.reader(csvFile)  # 读取文件数据
        for item in reader:
            if reader.line_num == 1:
                continue
            # 定义删除的字串列表
            replace_list = ['省', '市', '壮族自治区', '维吾尔自治区', '回族自治区', '自治区']
            # 调用删除字串的函数
            province_name = replace_something(item[0], replace_list)
            if len(result['province']) == 34:
                break
            if province_name in result['province']:
                continue
            else:
                result['province'].append(province_name)
                result['province_confirmedCount'].append(int(item[2]))
    # 绘制地图
    from pyecharts import options as opts
    from pyecharts.charts import Map

    map = Map()
    map.add("确诊人数", [list(z) for z in zip(result['province'], result['province_confirmedCount'])], 'china')
    map.set_global_opts(
        title_opts=opts.TitleOpts(title="疫情地图"),
        visualmap_opts=opts.VisualMapOpts(max_=2000),
    )
    map.render(path="疫情地图.html")

def display():
    draw()
    import webbrowser
    webbrowser.open("疫情地图.html")