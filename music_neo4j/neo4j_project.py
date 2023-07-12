import csv
import re
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo

# py2neo version = 2021.2.3
# neo4j community version = 5.9

g = Graph("bolt://localhost:7687", auth = ('neo4j','wang250188'))
g.run('match (n) detach delete n')

with open('./musicians_relationships_eng.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for item in reader:
        # 第一行是表格的属性
        if reader.line_num == 1:
            continue
        # print("line:", reader.line_num, "content:", item)
        head_node = Node('Composer', name = item[0])
        tail_node = Node('Composer', name = item[1])
        relation = Relationship(head_node, item[2], tail_node)
        
        g.merge(head_node, 'Composer', 'name')
        g.merge(tail_node, 'Composer', 'name')
        g.merge(relation, 'Composer', 'name')


# create(但实际上不会被用到)
def composer_add(name, birth='', death='', country=''):
    # 创建一个 Composer 节点
    c = Node("Composer", name=name)

    # 将节点添加到 Neo4j 图中
    g.create(c)
    return c


# read
def composer_query(name):
    query = "MATCH (c:Composer)"
    conditions = []
    if name:
        conditions.append(f"c.name =~ '(?i).*{re.escape(name)}.*'")  # 使用模糊匹配正则表达式
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " RETURN c"

    # 执行查询并返回结果
    result = g.run(query).data()
    return result

# update
def composer_update(name, new_name, birth='', death='', country='', new_birth='', new_death='', new_country=''):
    # 构建 Cypher 更新语句
    # cypher_query = """
    #     MATCH (c:Composer {name: $name, birth: $birth, death: $death, country: $country})
    #     SET c.name = $new_name, c.birth = $new_birth, c.death = $new_death, c.country = $new_country
    #     """
    
    
    # 执行查询
    # g.run(cypher_query, name=name, birth=birth, death=death, country=country,
    #           new_name=new_name, new_birth=new_birth, new_death=new_death, new_country=new_country)

    cypher_query = f"""
        MATCH (c:Composer)
        WHERE c.name =~ '(?i).*{re.escape(name)}.*'
        SET c.name = $new_name
        """

    # 执行更新
    g.run(cypher_query, new_name=new_name)

# delete
def composer_delete(name, birth='', death='', country=''):
    # 构建 Cypher 删除语句
    cypher_query = f"""
        MATCH (c:Composer)
        WHERE c.name =~ '(?i).*{re.escape(name)}.*'
        OPTIONAL MATCH (c)-[r]-()
        DELETE c, r
        """

    # 执行查询
    g.run(cypher_query)


# do some test
# print(composer_query("chopin"))

# composer_update('chopin', 'XXXX')
# print(composer_query('XXXX'))

# composer_delete('XXX')
# print(composer_query('XXXX'))