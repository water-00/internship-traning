import json

# 假设你有一个包含Cypher查询的字符串
cypherString = "match(c:Composer) return c;"

# 创建一个字典，将Cypher查询字符串作为其中一个键值对的值
cypher_dict = {
    "cypherString": cypherString
}

# 将字典转换为JSON格式
json_data = json.dumps(cypher_dict, indent=2)

# 打印JSON格式数据
print(json_data)