from py2neo import Graph, Node, Relationship

graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))

# 打印节点的 id 和属性


# 创建两个节点
# person_node = Node("Person", name="John")
# company_node = Node("Company", name="ABC Corp")

# 好像不需要使用create

# graph.create(company_node)
# # 创建一个关系
# works_at = Relationship(person_node, "WORKS_AT", company_node, years=5)
#
# # 将关系添加到图数据库
# graph.create(works_at)
#
# results = graph.run("MATCH (n) RETURN n")
#
# for result in results:
#     print(result)

def db_init():
    piece_init = '''
    LOAD CSV WITH HEADERS FROM 'file:///piece.csv' AS row
    CREATE (:Piece {opus: row.opus, name: row.name, composer: row.composer, album: row.album})
    '''
    graph.run(piece_init)

    composer_init = '''
    LOAD CSV WITH HEADERS FROM 'file:///composer.csv' AS row
    CREATE (:Composer {name: row.name, birth: row.birth, death: row.death, country: row.country})
    '''
    graph.run(composer_init)

    album_init = '''
    LOAD CSV WITH HEADERS FROM 'file:///album.csv' AS row
    CREATE (:Album {name: row.name, publish_time: row.publish_time, company: row.company, performer: row.performer})
    '''
    graph.run(album_init)

def piece_query(opus, name, composer, album):
    # 构建 Cypher 查询语句
    query = "MATCH (p:Piece)"
    conditions = []

    # 根据输入参数添加查询条件
    if opus:
        conditions.append(f"p.opus = '{opus}'")
    if name:
        conditions.append(f"p.name = '{name}'")
    if composer:
        conditions.append(f"p.composer = '{composer}'")
    if album:
        conditions.append(f"p.album = '{album}'")

    # 添加查询条件到 Cypher 查询语句
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " RETURN p"

    # 执行查询并返回结果
    result = graph.run(query).data()
    return result

def composer_query(name, birth, death, country):
    # 构建 Cypher 查询语句
    query = "MATCH (c:Composer)"
    conditions = []

    # 根据输入参数添加查询条件
    if name:
        conditions.append(f"c.name = '{name}'")
    if birth:
        conditions.append(f"c.birth = '{birth}'")
    if death:
        conditions.append(f"c.death = '{death}'")
    if country:
        conditions.append(f"c.country = '{country}'")

    # 添加查询条件到 Cypher 查询语句
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " RETURN c"

    # 执行查询并返回结果
    result = graph.run(query).data()
    return result

def album_query(name, publish_time, company, performer):
    # 构建 Cypher 查询语句
    query = "MATCH (a:Album)"
    conditions = []

    # 根据输入参数添加查询条件
    if name:
        conditions.append(f"a.name = '{name}'")
    if publish_time:
        conditions.append(f"a.publish_time = '{publish_time}'")
    if company:
        conditions.append(f"a.company = '{company}'")
    if performer:
        conditions.append(f"a.performer = '{performer}'")

    # 添加查询条件到 Cypher 查询语句
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " RETURN a"

    # 执行查询并返回结果
    result = graph.run(query).data()
    return result


def piece_add(opus, name, composer, album):
    # 创建一个 Piece 节点
    piece = Node("Piece", opus=opus, name=name, composer=composer, album=album)

    # 将节点添加到 Neo4j 图中
    graph.create(piece)

    return piece


def composer_add(name, birth, death, country):
    # 创建一个 Composer 节点
    composer = Node("Composer", name=name, birth=birth, death=death, country=country)

    # 将节点添加到 Neo4j 图中
    graph.create(composer)

    return composer

def ablum_add(name, publish_time, company, performer):
    # 创建一个 Album 节点
    album = Node("Album", name=name, publish_time=publish_time, company=company, performer=performer)

    # 将节点添加到 Neo4j 图中
    graph.create(album)

    return album


def piece_del(opus, name, composer, album):
    # 构建 Cypher 查询语句
    cypher_query = """
       MATCH (piece:Piece {opus: $opus, name: $name, composer: $composer, album: $album})
       DELETE piece
       """

    # 执行查询
    graph.run(cypher_query, opus=opus, name=name, composer=composer, album=album)

def composer_del(name, birth, death, country):
    # 构建 Cypher 查询语句
    cypher_query = """
       MATCH (composer:Composer {name: $name, birth: $birth, death: $death, country: $country})
       DELETE composer
       """

    # 执行查询
    graph.run(cypher_query, name=name, birth=birth, death=death, country=country)

def ablum_del(name, publish_time, company, performer):
    # 构建 Cypher 查询语句
    cypher_query = """
    MATCH (album:Album {name: $name, publish_time: $publish_time, company: $company, performer: $performer})
    DELETE album
    """

    # 执行查询
    graph.run(cypher_query, name=name, publish_time=publish_time, company=company, performer=performer)

def piece_update(opus, name, composer, album, new_opus, new_name, new_composer, new_album):
    # 构建 Cypher 查询语句
    cypher_query = """
        MATCH (piece:Piece {opus: $old_opus, name: $old_name, composer: $old_composer, album: $old_album})
        SET piece.opus = $new_opus, piece.name = $new_name, piece.composer = $new_composer, piece.album = $new_album
        """

    # 执行查询
    graph.run(cypher_query, old_opus=opus, old_name=name, old_composer=composer, old_album=album,
              new_opus=new_opus, new_name=new_name, new_composer=new_composer, new_album=new_album)

def composer_update(name, birth, death, country, new_name, new_birth, new_death, new_country):
    # 构建 Cypher 查询语句
    cypher_query = """
        MATCH (composer:Composer {name: $name, birth: $birth, death: $death, country: $country})
        SET composer.name = $new_name, composer.birth = $new_birth, composer.death = $new_death, composer.country = $new_country
        """

    # 执行查询
    graph.run(cypher_query, name=name, birth=birth, death=death, country=country,
              new_name=new_name, new_birth=new_birth, new_death=new_death, new_country=new_country)



def ablum_update(name, publish_time, company, performer, new_name, new_publish_time, new_company, new_performer):
    # 构建 Cypher 查询语句
    cypher_query = """
        MATCH (album:Album {name: $name, publish_time: $publish_time, company: $company, performer: $performer})
        SET album.name = $new_name, album.publish_time = $new_publish_time, album.company = $new_company, album.performer = $new_performer
        """

    # 执行查询
    graph.run(cypher_query, name=name, publish_time=publish_time, company=company, performer=performer,
              new_name=new_name, new_publish_time=new_publish_time, new_company=new_company,
              new_performer=new_performer)







