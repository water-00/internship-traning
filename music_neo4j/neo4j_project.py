import csv
import re
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo

# py2neo version = 2021.2.3
# neo4j community version = 5.9

g = Graph("bolt://localhost:7687", auth = ('neo4j','wang250188'))
g.run('match (n) detach delete n')


with open('./formatted_file.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for item in reader:
        # 第一行是表格的属性
        if reader.line_num == 1:
            continue
        head_node = Node('Person', name = item[0])
        tail_node = Node('Person', name = item[1])
        relation = Relationship(head_node, item[2], tail_node)
        
        g.merge(head_node, 'Person', 'name')
        g.merge(tail_node, 'Person', 'name')
        g.merge(relation, 'Person', 'name')

with open('./composer_info.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for item in reader:
        if reader.line_num == 1:
            continue
        query = "MATCH (p:Person {name: '" + item[0] + "'})RETURN p"
        result = g.run(query)

        for record in result:
            person_node = record["p"]
            person_node.add_label("Composer")
            person_node["birth day"] = item[1]
            person_node["death day"] = item[2]
            person_node["birth place"] = item[3]
            g.push(person_node)

with open('./piece.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for item in reader:
        if reader.line_num == 1:
            continue
        piece_node = Node('Piece', opus = item[0], name = item[1], composer = item[2], type = item[3])
        g.create(piece_node)
        query = "MATCH (c:Composer {name: '" + item[2] + "'})RETURN c"
        result = g.run(query)
        
        for record in result:
            composer_node = record['c']  # Assuming 'c' is the variable representing the Composer node
            relation = Relationship(composer_node, "创作", piece_node)
            g.create(relation)

# create
def create_person(name):
    c = Node("Person", name=name)
    g.create(c)
    return c

def create_composer(name, birth_day, death_day, birth_place):
    c = Node("Person", name=name)
    c.add_label("Composer")
    c["birth day"] = birth_day
    c["death day"] = death_day
    c["birth place"] = birth_place
    g.push(c)
    return c

def create_relationship(node1, node2, relation_str):
    relationship = Relationship(node1, relation_str, node2)
    g.create(relationship)
    
# read
def find_person(name):
    query = "MATCH (c:Person)"
    conditions = []
    if name:
        conditions.append(f"c.name =~ '(?i).*{re.escape(name)}.*'")  # 使用模糊匹配正则表达式
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " RETURN c"

    # 执行查询并返回结果
    result = g.run(query)
    nodes = []
    for record in result:
        node = record["c"]
        nodes.append(node)
    return nodes

# update
def update_person(name, new_name):
    cypher_query = f"""
        MATCH (c:Person)
        WHERE c.name =~ '(?i).*{re.escape(name)}.*'
        SET c.name = $new_name
        """

    # 执行更新
    g.run(cypher_query, new_name=new_name)
    

def update_composer(name, new_name, new_birth='', new_death='', new_birth_place=''):
    # 构建 Cypher 更新语句
    cypher_query = f"""
        MATCH (c:Person)
        WHERE c.name =~ '(?i).*{re.escape(name)}.*'
        SET c.name = $new_name, c.`birth day` = $new_birth, c.`death day` = $new_death, c.`birth place` = $new_birth_place
        """

    # 执行更新
    g.run(cypher_query, new_name=new_name, new_birth=new_birth, new_death=new_death, new_birth_place=new_birth_place)

# delete
def delete_person(name):
    # 构建 Cypher 删除语句
    cypher_query = f"""
        MATCH (c:Person)
        WHERE c.name =~ '(?i).*{re.escape(name)}.*'
        OPTIONAL MATCH (c)-[r]-()
        DELETE c, r
        """

    # 执行查询
    g.run(cypher_query)


# do some test
def example():
    # update & read
    print(find_person("chopin"))
    update_person('chopin', 'Chopin') # give Chopin a shorter name
    print(find_person("chopin"))
    update_composer('chopin', 'Chopin') # replace all informations of Chopin
    print(find_person("chopin"))

    # create
    A = create_composer("Composer A", '', '', '')
    B = create_person("Person B")
    chopin = find_person("chopin")[0]
    create_relationship(A, chopin, 'friend')
    create_relationship(B, chopin, 'friend')

    # delete
    a = A['name']; b = B['name']
    delete_person(a)
    delete_person(b)
    print(find_person(a)) # delete successfully
    print(find_person(b))
    
info = """
    You can manipulate this neo4j database in the following way:
    - create_person(name)
    - create_composer(name, birth_day, death_day, birth_place)
    - create_relationship(node1, node2, relation_str)
    - find_person(name)
    - update_person(name, new_name)
    - update_composer(name, new_name, new_birth='', new_death='', new_birth_place='')
    - delete_person(name)
    or you can run example() to test all the listed function.
"""
print(info)