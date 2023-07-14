import pandas as pd

## 一个将musicians_relationships_eng.csv转换为formatted_file.csv的小脚本，主要目的是修改一下名字格式

# 读取CSV文件
df = pd.read_csv('musicians_relationships_eng.csv')

# 定义一个函数，将名字格式化为"First Name Last Name"的形式
def format_name(name):
    parts = name.split(', ')
    first_name = parts[1]
    last_name = parts[0]
    formatted_name = f"{first_name} {last_name}"
    return formatted_name

# 在"head"和"tail"列上应用格式化函数
df['head'] = df['head'].apply(format_name)
df['tail'] = df['tail'].apply(format_name)

# 保存修改后的CSV文件
df.to_csv('formatted_file.csv', index=False)
