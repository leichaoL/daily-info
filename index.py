
import time
from datetime import date, datetime
import requests
from notion_client import Client
import config

corpid = config.get("corpid")
corpsecret = config.get("corpsecret")
agentid = config.get("agentid")
notionsecret = config.get('notionsecret')
databaseid = config.get('databaseid')

# notionsecret = "secret_as3cj6Rg9fY5pE2NXyY9EmZe2kO8b4UlctTgI6ZKfib"
# databaseid = "ef4eadd8f84d4dee803a2681d1749e0f"
# agentid = '1000002'



notion = Client(auth=notionsecret)
today_str = date.today().strftime("%Y-%m-%d")



def get_notion_page(date):
    filter = {"property": 'Date', 'date': {'equals': date}}
    results = notion.databases.query(database_id = databaseid, filter = filter, page_size = 1).get('results')
    if results:
        page = results[0]
        page_id = page.get('id')
        page_status = page.get('properties').get('Published').get('checkbox')
        page_cover = page.get('properties').get('Cover').get('files')[0]
        cover_type = page_cover.get('type')
        cover_url = page_cover.get(cover_type).get('url')
        page_title = page['properties']['Page']['title'][0]['plain_text']
        page_desc = page['properties']['Description']['rich_text'][0]['plain_text']
        page_url = page.get('url')
    else:
        page_id = None
        page_status = False
        page_title = None
        page_desc = None
        cover_url = None
        page_url = None

    return page_id, page_status, page_title, page_desc, cover_url, page_url





def main():
    old_status = get_notion_page(today_str)[1]
    while (datetime.now().hour >= 12) & (datetime.now().hour < 18):
        new_status = get_notion_page(today_str)[1]
        if (new_status != old_status) & (new_status == True):
            old_status = new_status

            if corpid and corpsecret and agentid:
                data = handle_message(today_str)
                token = get_token(corpid, corpsecret)
                if token is None:
                    return 0
                url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
                res = requests.post(url, json=data).json()
                if res["errcode"] == 0:
                    print("企业微信消息发送成功")
                    return 1
                elif res["errcode"] != 0:
                    print("企业微信消息发送失败: "+str(res))
                    return 0
            else:
                print("企业微信机器人配置缺失")
                return 0

        elif (new_status != old_status) & (new_status == False):
            old_status = new_status
        time.sleep(5)



# 处理信息


def handle_message(date):
    __, __, page_title, page_desc, cover_url, page_url = get_notion_page(date)

    article = [{
        "title": page_title,
        "description": page_desc,
        "url": page_url,
        "picurl": cover_url
    }]
    msg = {
        "touser": "@all",
        "toparty": "",
        "totag": "",
        "msgtype": "news",
        "agentid": agentid,
        "news": {
            "articles": article
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    return msg


# 获取调用接口凭证


def get_token(corpid, corpsecret):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    values = {
        "corpid": corpid,
        "corpsecret": corpsecret,
    }
    res = requests.get(url, params=values).json()
    if res["errcode"] == 0:
        return res["access_token"]
    else:
        print("企业微信access_token获取失败: " + str(res))
        return None



# # 主函数


# def main():
#     if corpid and corpsecret and agentid:
#         data = handle_message()
#         token = get_token(corpid, corpsecret)
#         if token is None:
#             return 0
#         url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
#         res = requests.post(url, json=data).json()
#         if res["errcode"] == 0:
#             print("企业微信消息发送成功")
#             return 1
#         elif res["errcode"] != 0:
#             print("企业微信消息发送失败: "+str(res))
#             return 0
#     else:
#         print("企业微信机器人配置缺失")
#         return 0





if __name__ == "__main__":
    main()
