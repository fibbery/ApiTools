import requests

# 获取查询targetstore权限token
def accsess_token(url, usr, pwd):

    payload = "{'file_type': 'CCL', 'with_vc': 'true'}"
    response = requests.request("POST", url, data=payload, auth=(usr, pwd))
    return (response.json())

# 判断环境变量
def host(env):

    if env == "svr":
        # 正式环境
        return "https://svr14s.localgravity.com"
    elif env == "stg":
        # 测试环境
        return "https://stg14s.localgravity.com"

# 账号密码
def accounts(env, modules):

    if modules == "sys_flow":
        pass