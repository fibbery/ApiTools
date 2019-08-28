"""
用户开通targetstore权限时，需要将账号及对应的权限信息提交给Sheila
Sheila将数据导入后，先在测试环境（stg）中检查账号权限是否开通
确认没问题后，通知Sheila可以放到线上了。过段时间再去检查是否被推到了线上环境（svr）

查看账号权限，需要先登录，获取了token之后，才能调用query接口
"""

from utils.tools import accsess_token, host
import requests
import pandas as pd

# 选择环境
host = host("svr")

# 获取token接口
url_l = host + "/apic/login"
# 查询接口
url_q = host + "/apic/v1/permissions/query"

# 输入对应账号密码，以获取token
token = accsess_token(url_l, "SYSTEM_FLOW", "p#tSiG_ydLi!31*F")

headers = {
    'Authorization': "{}{}".format('Bearer ', token['access_token'])
    }

# 读取csv文件
path = '../datas/tsdatas.csv'
datas = pd.read_csv(path)
# 存放没开通权限的账号
invalid = []

# 依次输入需要查询权限的账号
for i in datas['email']:
    payload = '{"user_login": "' + i + '"}'
    # 发送post请求，将返回的响应存入response
    response = requests.request("POST", url_q, data=payload, headers=headers)
    # 输出没有开通权限的账号
    if response.status_code == 401:
        print('Need to check {} ! {}'.format(i, response.text))
        invalid.append(i)
    else:
        print(response.text)

# 将没权限的账号写入新的csv文档
if invalid:
    df = pd.DataFrame(data = invalid, columns= ['email'])
    df.to_csv('../reports/invalid.csv', index = False)