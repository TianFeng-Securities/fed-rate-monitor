import requests
from lxml import etree
import os


class ItemCardWrapper(object):
    date = ''
    target_interest_list = []

    def __init__(self, date, target_interest_list):
        self.date = date
        self.target_interest_list = target_interest_list


class ItemTargetInterest(object):
    name = '1.50 - 1.75'  # 默认为此利率，‘1.75 - 2.00’为一档，表示加息一次；‘1.25 - 1.50’为一档，表示减息一次；其他以此类推
    prob = None

    def __init__(self, name, prob):
        self.name = name
        self.prob = prob


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    content = response.content.decode("utf-8")
    html = etree.HTML(content)  # 转化为lxml的html，加快解析速度
    return html


url = "https://cn.investing.com/central-banks/fed-rate-monitor"
main_html = get_html(url)
# 会议集合
item_card_wrapper_list = main_html.xpath("//div[@class='cardWrapper']")
ItemCardWrapperList = []
for index, item_card_wrapper in enumerate(item_card_wrapper_list):
    date = item_card_wrapper.xpath(
        "//div[@id='cardName_%d']/text()" % (index))[0].strip()  # 这个时间为美联储议息会议时间
    ele_trs = item_card_wrapper.xpath(
        "//div[@id='search_section_%d']/table/tbody/tr" % (index))
    ItemTargetInterestList = []
    for ele_tr in ele_trs:
        name = ele_tr.getchildren()[0].text.strip()
        prob = ele_tr.getchildren()[1].text.strip()
        ItemTargetInterestList.append(ItemTargetInterest(name, prob))
    ItemCardWrapperList.append(ItemCardWrapper(date, ItemTargetInterestList))

update_date = main_html.xpath(
    "//*[@id='search_section_0']/div[4]")[0].text.strip()
print("更新时间", update_date)
for item_card_wrapper in ItemCardWrapperList:
    print(item_card_wrapper.date)
    for i in item_card_wrapper.target_interest_list:
        print(i.name, i.prob)
with open(update_date+".txt", 'w') as data:
    data.write(update_date+"\n")
    for item_card_wrapper in ItemCardWrapperList:
        data.write(item_card_wrapper.date+"\n")
        for i in item_card_wrapper.target_interest_list:
            data.write(i.name+" "+i.prob+"\n")
print("输出结果成功!")
os.system("pause")