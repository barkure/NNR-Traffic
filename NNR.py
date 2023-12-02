import requests
import json
import pandas as pd

payload = ""
headers = {
   'token': '', # 请在此处填入你的token
   'content-type': 'application/json',
}

# 获取所有规则
resp1 = requests.request("POST", "https://nnr.moe/api/rules", headers=headers, data=payload)
resp1_dict = json.loads(resp1.text)
data1 = resp1_dict['data']

# 获取所有可使用节点
resp2 = requests.request("POST", "https://nnr.moe/api/servers", headers=headers, data=payload)
resp2_dict = json.loads(resp2.text)
data2 = resp2_dict['data']
# 将所有节点的 sid、name、mf（倍率） 三个键值对提取出来
keys2 = ['sid', 'name', 'mf']
for item in data2:
    dict2 = {key: item[key] for key in keys2}

# 要输出的 所有规则 中的键
keys1 = ['name', 'sid', 'remote', 'rport', 'traffic']
# 创建一个空列表来存储最后要输出的数据
new_dicts = []
# 遍历data1（所有规则）列表
for item1 in data1:
    # 对于每个数据体，选择你需要的键并创建一个新的字典
    new_dict = {key: item1[key] for key in keys1}
    # 原本的流量单位是B，转换为GB
    new_dict['实际流量（GB）'] = item1['traffic'] / 1_000_000_000
    # 遍历data2（所有节点）列表，找到sid相同的节点，提取出mf（倍率）和name（节点名称）
    for item2 in data2:
        if item1['sid'] == item2['sid']:
            mf = item2['mf']
            name = item2['name']
            new_dict['节点名称'] = name
            new_dict['倍率'] = mf
            new_dict['结算流量（GB）'] = new_dict['实际流量（GB）'] * mf
    # 将新的字典添加到列表中
    new_dicts.append(new_dict)

# 将列表转换为DataFrame
df = pd.DataFrame(new_dicts)

# 将DataFrame写入Excel文件
df.to_excel('output.xlsx', index=False)