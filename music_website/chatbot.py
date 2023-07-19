#!/usr/bin/env python
# coding: utf-8


import os
import csv
import ahocorasick
from py2neo import Graph
from collections import defaultdict
'''问题分类'''
class QuestionClassifier:
    def __init__(self):
        # 实体列表
        self.person_eng_list = []
        self.person_ch_list = []
        self.person_relation_list = []
        self.type_ch_list = []
        self.type_eng_list = []
        self.piece_list = []
        # 特征词列表
        self.person_words = []
        self.type_words = []
        self.piece_words = []
        self.relation_words = []
        self.words = []
        # 构建词典
        self.person_dic = {}
        self.type_dic = {}
        self.relation_dic = {}
        # 问句疑问词
        self.list_qwds = ['哪些','有什么','列举','有啥','推荐']
        self.relation_qwds = ['是谁','关系','联系','谁是','和谁','有关','有谁','哪些人','什么人','人际']
        self.time_qwds = ['时间','时候','哪年','哪一年','年代','日子','时期','年份','何时','几时','年月']
        self.birth_qwds = ['出生','生于','诞生']
        self.death_qwds = ['死亡','死于','死了','逝世','去世','离世']
        self.place_qwds = ['哪里','地方','在哪','城市','国家','故乡']
        self.piece_qwds = ['写了','作了','几首','曲子','作品','创作']
        # 读取文件，对上述变量进行初始化
        self.readcsv()
        self.wordtype_dic = self.build_wdtype_dict()
        # 构造领域actree，提高检索效率
        self.region_tree = self.build_actree(list(self.words))
        print('model init finished ......')
        return
    
    '''文件读取'''
    def readcsv(self):
        # 构建人物和曲子类型的中英文对照字典
        with open('formatted_file.csv', 'r',encoding='utf-8') as file_eng:
            reader_eng = csv.reader(file_eng)
            next(reader_eng)
            for row in reader_eng:
                self.person_eng_list.append(row[0])
                self.person_eng_list.append(row[1])
                self.person_relation_list.append(row[2])
                temp = []
                temp.append(row[2])
                self.relation_dic[row[2]] = temp
        
        with open('musicians_relationships.csv', 'r',encoding='utf-8') as file_ch:
            reader_ch = csv.reader(file_ch)
            next(reader_ch)
            for row in reader_ch:
                self.person_ch_list.append(row[0])
                self.person_ch_list.append(row[1])

        for i in range(len(self.person_eng_list)):
            self.person_dic[self.person_ch_list[i]] = self.person_eng_list[i]
            self.person_dic[self.person_eng_list[i]] = self.person_eng_list[i]
        # 去重
        self.person_ch_list=list(set(self.person_ch_list))
        self.person_eng_list = list(set(self.person_eng_list))
        self.person_relation_list = list(set(self.person_relation_list))
        # 额外添加内容
        self.person_dic['莫扎特'] = "Wolfgang Amadeus Mozart"
        self.person_ch_list.append('莫扎特')
        self.person_dic['巴赫'] = "Johann Sebastian Bach"
        self.person_ch_list.append('巴赫')
        # 获取作品类别字典
        with open('chinese_english_trans.csv', 'r',encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                self.type_dic[row[0]] = row[1]
                self.type_dic[row[1]] = row[1]
                self.type_ch_list.append(row[0])
                self.type_eng_list.append(row[1])
        # 获取作品信息
        with open('piece.csv', 'r',encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.piece_list.append(row[1])
        
        self.piece_list = list(set(self.piece_list))
        # 特征词
        self.person_words = self.person_eng_list + self.person_ch_list
        self.type_words = self.type_ch_list + self.type_eng_list
        self.piece_words = self.piece_list
        self.relation_words = self.person_relation_list
        for word in self.person_relation_list:
            if "、" in word:
                splitted = word.split("、")
                self.relation_words.append(splitted[0])
                self.relation_words.append(splitted[1])
        # 字典额外添加内容
        self.relation_words.append('创作')
        self.relation_words.append('朋友')
        self.relation_words.append('亲人')
        self.relation_dic['朋友'] = ['好友','至交','好友、出版商','好友、合伙人']
        self.relation_dic['好友'] = ['好友','至交','好友、出版商','好友、合伙人']
        self.relation_dic['出版商'] = ['好友、出版商']
        self.relation_dic['合伙人'] = ['好友、合伙人']
        self.relation_dic['亲人'] = ['父亲','夫妻','女婿']
        self.relation_words=list(set(self.relation_words))
    
    '''将问题进行分类'''
    def classify(self, question):
        data = {}
        # 提取问题中的实体
        question_entity = []
        for each in self.region_tree.iter(question):
            entity = each[1][1]
            question_entity.append(entity)
        question_entity_dict = {each:self.wordtype_dic[each] for each in question_entity}
        data['args'] = question_entity
        data['question_entity_dict'] = question_entity_dict

        # 提取问题相关的待查询关系
        types = []  # 问题中涉及的实体类别
        for each in question_entity_dict.values():
            types.extend(each)        
        question_type = 'unknow'
        question_types = []
        
        #确定问题类型
        # 作曲家-作品列举
        if self.check_words(self.list_qwds, question) and ('person' in types):
            if self.check_words(self.piece_qwds, question):
                if 'type' in types:
                    question_type = 'composer_specific_type_pieces'
                else:
                    question_type = 'composer_pieces'
                question_types.append(question_type)
            elif 'type' in types:
                question_type = 'composer_specific_type_pieces'
                question_types.append(question_type)
            
        # 作曲家-作曲家关系
        if self.check_words(self.relation_qwds, question) and ('person' in types):
            if 'relation' in types:
                question_type = 'composer_specific_relation'
            elif types.count('person') >= 2:
                question_type = 'multy_composer_relations'
            else:
                question_type = 'composer_all_relation'
            question_types.append(question_type)
            
        # 作曲家出生
        if self.check_words(self.birth_qwds, question) and ('person' in types):
            if self.check_words(self.time_qwds, question):
                question_type = 'birth_time'
            elif self.check_words(self.place_qwds, question):
                question_type = 'birth_place'
            else:
                question_type = 'unknow'
            question_types.append(question_type)

        # 作曲家死亡
        if self.check_words(self.death_qwds, question) and ('person' in types):
            if self.check_words(self.time_qwds, question):
                question_type = 'death_time'
            else:
                question_type = 'unknow'
            question_types.append(question_type)        
        
        # 没有查到对应问题
        if question_types == [] or question_types == ['unknow']:
            # 出现了人名
            if 'person' in types:
                # 出现了某个特定类型曲子类型，返回此人写的该类型曲子
                if 'type' in types:
                    question_type = 'composer_specific_type_pieces'
                # 出现了曲子相关的描述，返回此人所有作的曲子
                elif self.check_words(self.piece_qwds, question):
                    question_type = 'composer_pieces'
                # 出现了某一关系，返回和此人有该关系的路径
                elif 'relation' in types:
                    question_type = 'composer_specific_relation'
                # 都没有，直接返回该人的节点相关信息
                else:
                    question_type = 'composer_info'
            question_types.append(question_type)

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        
        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = {}
        self.words = set(self.person_words + self.type_words + self.piece_words + self.relation_words + self.relation_qwds)
        for word in self.words:
            wd_dict[word] = []
            if word in self.person_words:
                wd_dict[word].append('person')
            if word in self.type_words:
                wd_dict[word].append('type')
            if word in self.piece_words:
                wd_dict[word].append('piece')
            if word in self.relation_words:
                wd_dict[word].append('relation')
            if word in self.relation_qwds:
                wd_dict[word].append('relation_qwds')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


'''根据问题类别生成查询语句'''
class QuestionPaser:

    '''解析主函数'''
    def parser_main(self, classifier,res_classify):
        args = res_classify['args']
        question_types = res_classify['question_types']
        entity_dict = res_classify['question_entity_dict']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = self.sql_transfer(classifier,entity_dict, question_type, args)
            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, classifier, entity_dict, question_type, entities):
        if not entities:
            return []
        # 查询语句
        sql = []
        # 查询某一作曲家写了哪些特定类型曲目
        if question_type == 'composer_specific_type_pieces':
            composers = []
            types = []
            for i in entities:
                if 'person' in entity_dict[i]:
                    composers.append(classifier.person_dic[i])
                elif 'type' in entity_dict[i]:
                    types.append(classifier.type_dic[i])
                else:
                    continue
            sql = "MATCH (m:Piece) where m.composer in {0} and m.type in {1} return m".format(composers,types)
        
        # 查询某一作曲家的全部曲目
        elif question_type == 'composer_pieces':
            composers = []
            for i in entities:
                if 'person' in entity_dict[i]:
                    composers.append(classifier.person_dic[i])
                else:
                    continue
            sql = "MATCH (m:Piece) where m.composer in {0} return m".format(composers)
        
        # 查询多个人之间的关系
        elif question_type == 'multy_composer_relations':
            people = []
            for i in entities:
                if 'person' in entity_dict[i]:
                    people.append(classifier.person_dic[i])
                else:
                    continue
            sql = "MATCH p=(n)--(m) where n.name in {0} and m.name in {0} return p".format(people)
        
        # 查询某人的特定关系人（比如：贝多芬的老师是谁）
        elif question_type == 'composer_specific_relation':
            people = []
            relations = []
            people_indexs = []
            relation_indexs = []
            qwds_index = -1
            for i in range(len(entities)):
                if 'person' in entity_dict[entities[i]]:
                    people.append(classifier.person_dic[entities[i]])
                    people_indexs.append(i)
                elif 'relation' in entity_dict[entities[i]]:
                    relations.extend(classifier.relation_dic[entities[i]])
                    relation_indexs.append(i)
                elif 'relation_qwds' in entity_dict[entities[i]]:
                    qwds_index=i
                else:
                    continue
            max_val = max(max(people_indexs), max(relation_indexs))
            min_val = min(min(people_indexs), min(relation_indexs))
            if qwds_index<max_val and qwds_index>min_val:  # 贝多芬是谁的老师
                sql="MATCH p=(n)-[r]->(m) where n.name in {0} and type(r) in {1} return p".format(people,relations)
            else:  # 贝多芬的老师是谁
                sql="MATCH p=(m)-[r]->(n) where n.name in {0} and type(r) in {1} return p".format(people,relations)
        
        # 查询所有跟某人有关系的人
        elif question_type == 'composer_all_relation':
            people = []
            for i in entities:
                if 'person' in entity_dict[i]:
                    people.append(classifier.person_dic[i])
                else:
                    continue
            sql = "MATCH p=(n)--(m:Person) where n.name in {0} return p".format(people)
        
        # 查询出生时间
        elif question_type == 'birth_time':
            people = []
            for i in entities:
                if 'person' in entity_dict[i]:
                    people.append(classifier.person_dic[i])
                else:
                    continue
            sql = "MATCH (n:Person) where n.name in {0} return [n.name,n.`birth day`]".format(people)
        
        # 查询出生地点
        elif question_type == 'birth_place':
            people = []
            for i in entities:
                if 'person' in entity_dict[i]:
                    people.append(classifier.person_dic[i])
                else:
                    continue
            sql = "MATCH (n:Person) where n.name in {0} return [n.name,n.`birth place`]".format(people)
        
        # 查询去世时间
        elif question_type == 'death_time':
            people = []
            for i in entities:
                if 'person' in entity_dict[i]:
                    people.append(classifier.person_dic[i])
                else:
                    continue
            sql = "MATCH (n:Person) where n.name in {0} return [n.name,n.`death day`]".format(people)
        
        # 查询个人信息
        elif question_type == 'composer_info':
            people = []
            for i in entities:
                if 'person' in entity_dict[i]:
                    people.append(classifier.person_dic[i])
                else:
                    continue
            sql = "match (n:Person) where n.name in {0} return n".format(people)
        return sql



'''生成回答'''
class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt: // localhost:7687", auth=("neo4j", "wang250188"))

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls,question):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = [sql_['sql']]
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers,question)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers, question):
        if not answers:
            final_answer="抱歉，没有找到关于“{0}”问题的结果😭。您可以试试换一个问题。".format(question)
            return final_answer
        # 根据问题种类按照不同格式回答
        
        # 查询某一作曲家写了哪些特定类型曲目
        if question_type == 'composer_specific_type_pieces':
            # 创建默认值为列表的字典，对应每个作曲家的作品列表
            composer_dic = defaultdict(list)
            for data in answers:
                node = data['m']
                composer_dic[node['composer']].append({'name':node['name'],'opus':node['opus'],'type':node['type']})
            final_answer = "您好！关于您给出的问题“{0}”，这是我查阅数据库的返回结果😊！".format(question)
            for key,value in composer_dic.items():
                final_answer += "\n作曲家{0}的作品有：".format(key)
                for piece in value:
                    final_answer += "\n  名称：{0} opus编号：{1} 类型：{2}".format(piece['name'],piece['opus'],piece['type'] if piece['type'] != '' else "other")
            final_answer += "\n您还可以通过查阅作品的编号以获取更多详细信息，欢迎您继续提问我😀！"
        
        # 查询某一作曲家的全部曲目
        elif question_type == 'composer_pieces':
            composer_dic = defaultdict(list)
            for data in answers:
                node = data['m']
                composer_dic[node['composer']].append({'name':node['name'],'opus':node['opus'],'type':node['type']})
            final_answer = "您好！关于您给出的问题“{0}”，这是我查阅数据库的返回结果😊！".format(question)
            for key,value in composer_dic.items():
                final_answer += "\n作曲家{0}的作品有：".format(key)
                for piece in value:
                    final_answer += "\n  名称：{0} opus编号：{1} 类型：{2}".format(piece['name'],piece['opus'],piece['type'] if piece['type'] != '' else "other")
            final_answer += "\n您还可以通过查阅作品的编号以获取更多详细信息，欢迎您继续提问我😀！"
        
        # 查询多个人之间的关系
        elif question_type == 'multy_composer_relations':
            final_answer = "您好！关于您给出的问题“{0}”，我查到了他们之间有以下关系😊".format(question)
            for data in answers:
                path = data['p']
                final_answer += "\n  " + str(path)
            final_answer += "\n我还给出了他们的关系图，您也可以通过下图来了解他们之间的关系😊，欢迎继续提问😀！"
            
        # 查询某人的特定关系人
        elif question_type == 'composer_specific_relation':
            final_answer = "您好！关于您给出的问题“{0}”，我查出了以下相关人物😊，他们和您问题中涉及的人物的关系如下：".format(question)
            for data in answers:
                path = data['p']
                final_answer += "\n  " + str(path)
            final_answer += "\n我还给出了他们的关系图，您也可以通过下图来了解他们之间的关系😊，欢迎继续提问😀！"
        
        # 查询所有跟某人有关系的人
        elif question_type == 'composer_all_relation':
            final_answer = "您好！关于您给出的问题“{0}”，我查到了以下相关人物😊，他们和您问题中涉及的人物的关系如下：".format(question)
            for data in answers:
                path = data['p']
                final_answer += "\n  " + str(path)
            final_answer += "\n我还给出了他们的关系图，您也可以通过下图来了解他们之间的关系😊，欢迎继续提问😀！"
            
        # 查询出生时间
        elif question_type == 'birth_time':
            final_answer = ""
            for data in answers:
                info = data['[n.name,n.`birth day`]']
                person = info[0]
                time = info[1]
                final_answer += "{0}的出生时间为{1}。\n".format(person,time)         
            final_answer += "欢迎继续提问🙂。"
            
        # 查询出生地点
        elif question_type == 'birth_place':
            final_answer = ""
            for data in answers:
                info = data['[n.name,n.`birth place`]']
                person = info[0]
                place = info[1]
                final_answer += "{0}的出生地点为{1}。\n".format(person,place)         
            final_answer += "欢迎继续提问🙂。"
        
        # 查询去世时间
        elif question_type == 'death_time':
            final_answer = ""
            for data in answers:
                info = data['[n.name,n.`death day`]']
                person = info[0]
                time = info[1]
                final_answer += "{0}的去世时间为{1}。\n".format(person,time)         
            final_answer += "欢迎继续提问🙂。"
            
        # 查询个人信息
        elif question_type == 'composer_info':
            final_answer = ""
            for data in answers:
                label = str(data['n'].labels)
                name = data['n']['name']
                if 'Composer' in label:
                    birth_time = data['n']['birth day']
                    birth_place = data['n']['birth place']
                    death_time = data['n']['death day']
                    final_answer += "{n}是一位伟大的作曲家，他于{t}出生于{p}，于{d}逝世。\n{n}的一生创作了很多的曲目，您可以通过搜索如“XXX写过哪些曲子？”这类问题来快速了解他的作品。\n您也可以通过搜索“XXX的人际关系？”这类问题来快速了解他的人际关系😊。\n欢迎继续向我提问😀！".format(n=name,t=birth_time,p=birth_place,d=death_time)
                else:
                    final_answer += "抱歉，我没有查到关于{n}的更多信息😔，您可以搜索“XXX的人际关系？”这类问题来了解他的人际关系。".format(n=name)
        return final_answer


# 问答机器人主体
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()  # 问题分类模块
        self.parser = QuestionPaser()  # 查询语句生成模块
        self.searcher = AnswerSearcher()  # 回答语句生成模块
    
    def get_query(self, question):
        res_classify = self.classifier.classify(question)
        res_cypher = self.parser.parser_main(self.classifier,res_classify)
        return res_classify,res_cypher
    
    def get_answer(self,res_cypher,question):
        final_answers = self.searcher.search_main(res_cypher,question)
        return final_answers


chatbot = ChatBotGraph()

# Placeholder for the chatbot logic
def chatbot_response(question):
    print(question)
    res_classify,res = chatbot.get_query(question)
    answer = chatbot.get_answer(res,question)
    response = answer[0]
    return response

test_str = "你好"
answer = chatbot_response(test_str)
print(answer[0])

# questions = ["贝多芬有哪些奏鸣曲？",
#             "贝多芬写了什么曲子？",
#             "推荐一些贝多芬和肖邦的协奏曲",
#             "有没有舒伯特的曲子？",
#             "李斯特的舞曲和协奏曲",
#             "莫扎特",
#             "贝多芬是谁的老师？",
#             "贝多芬的老师是谁？",
#             "谁是贝多芬的老师？",
#             "贝多芬的人际关系",
#             "贝多芬、莫扎特和安东尼奥·萨列里是什么关系？",
#             "贝多芬的老师和朋友都有谁？",
#             "肖邦的朋友",
#             "舒曼和谁有关系？",
#             "柴可夫斯基和舒伯特在哪里出生？",
#             "贝多芬于哪一年逝世？",
#             "我想了解贝多芬的相关信息"]
# for question in questions:
#     print('================='+question+'======================')
#     res_classify,res = chatbot.get_query(question)
#     print("查询语句：")
#     print(res[0]['sql'])
#     #print(res)
#     answer = chatbot.get_answer(res,question)
#     print("输出回答：")
#     print(answer[0])