import jieba
import os
from collections import defaultdict
import math

# 数据文件路径
path = "results/"
files = os.listdir(path)
# 添加自定义字典
jieba.load_userdict('./resource/dict_file.txt')


# 创建文档列表
def create_docu_set():
    docu_set = {}
    i = 0
    for f in files:
        if f != ".DS_Store" and f != ".gitkeep":
            docu_set.update({i: f})
            i = i + 1
    return docu_set


# 创建停用词列表
def stop_words_list():
    stopwords = [line.strip() for line in open('resource/stop_words.txt', 'r', encoding='utf-8').readlines()]
    return stopwords


# 判断是否为中文字符串
def isCh(word):
    res = True
    for w in word:
        if not '\u4e00' <= w <= '\u9fff':
            res = False
    return res


# 判断是否为英文字符串
def isAl(word):
    res = False
    for w in word:
        if (u'\u0041' <= w <= u'\u005a') or (u'\u0061' <= w <= u'\u007a'):
            res = True
    return res


# 判断是否为数字
def isNum(word):
    res = False
    for w in word:
        if u'\u0030' <= w <= u'\u0039':
            res = True
    return res


# 分词
def seg_sentence(inputs):
    sentence = jieba.cut(inputs.strip(), cut_all=False)
    stopwords = stop_words_list()
    words = []
    for word in sentence:
        flag_1 = isCh(word)
        flag_2 = isAl(word)
        flag_3 = isNum(word)
        if flag_1 or flag_2 or flag_3:
            if word not in stopwords and word != ' ':
                words.append(word)
    return words


# 构建总的词汇表
def get_all_words():
    all_words = []
    for i in files:
        # 逐个读取文件的内容
        f = open(path + '/' + i, 'r')
        for line in f:
            words = seg_sentence(line)
            all_words.extend(words)
    # 转换为set(去重)
    all_words = set(all_words)
    # all_words = list(all_words)
    return all_words


# 构建某个文档的词汇表
def get_text_words(name):
    text_words = []
    for i in files:
        if i == name:
            f = open(path + '/' + i, 'r', encoding='utf-8')
            for line in f:
                words = seg_sentence(line)
                text_words.extend(words)
    text_words = set(text_words)
    return text_words


# 获取倒排索引
def get_inverse_index(docu_set):
    inverse_index = defaultdict(list)
    # 遍历所有的文档
    for d in docu_set.keys():
        text_name = docu_set[d]
        # 当前文档的词汇表
        if d % 10 == 0:
            progress: str = format(float(d) / float(len(docu_set.keys())), '.2%')
            print('[INFO] progress: ' + progress + ' ' + str(d) + ' of ' + str(len(docu_set.keys())))
        text_words = get_text_words(text_name)
        # 遍历当前文档的词汇表
        for w in text_words:
            # 如果当前词已经在索引字典中了
            if w in inverse_index.keys():
                inverse_index[w].append(d)
            else:
                inverse_index.update({w: [d]})

    return inverse_index


# 创建索引文件
def create_inverse_txt():
    inverse_index = get_inverse_index(create_docu_set())
    f = open('resource/inverse_index.txt', 'w')
    for k, v in inverse_index.items():
        f.write(k + ' ')
        for i in v:
            s = str(i)
            f.write(s + ' ')
        f.write('\n')
    f.close()


# 检索索引文件
def search_index(query_word):
    temp = []       # 用来存放找到的文件索引
    f = open('resource/inverse_index.txt', 'r')
    line = f.readline()
    while line:
        line = line.split()
        k = line[0]
        length = len(line)

        if query_word == k:
            i = 1
            while i < length:
                temp.append(line[i])
                i += 1
            break
        line = f.readline()
    f.close()
    return temp


# 计算词项在文档中的词频
def compute_tf(word, text_words):
    tf = 0
    length = len(text_words)
    for w in text_words:
        if w == word:
            tf += (1.0/length)
    return tf


# 计算逆文档频率
def compute_idf(word, docu_set):
    total = len(docu_set)
    num = len(search_index(word))
    idf = math.log(total/(1.0 + num))
    return idf


# 计算tf-idf
def compute_tfidf(tf, idf):
    return tf * idf


# 返回包含查询关键词的文档列表
def get_similar_texts(query):
    # 对查询字符串进行分词
    seg_words = seg_sentence(query)
    # 获取包含关键词的文档列表
    text_list = []
    for i in seg_words:
        temp = search_index(i)
        text_list.extend(temp)
    return text_list


# 获取相关度
def get_similarity(docu_set, keywords, text_list):
    similarity = {}
    for f in text_list:
        index = int(f)
        name = docu_set[index]
        text_words = get_text_words(name)
        tf_idf = 0.0
        for w in keywords:
            tf = compute_tf(w, text_words)
            idf = compute_idf(w, docu_set)
            tf_idf += compute_tfidf(tf, idf)
        if tf_idf > 0.015:
            similarity[name] = tf_idf
        if name.strip('.txt') == w:
            similarity[name] += 0.1
    return similarity


# 产生返回结果内容
def get_result(similarity, title, keywords):
    result = {}

    # 获取文档内容
    f1 = open(path + '/' + title, 'r')
    content = f1.read()
    f1.close()

    f2 = open('resource/index.txt', 'r')
    line = f2.readline()
    while line:
        line = line.split()
        k = line[0]
        if title.strip('.txt') == k:
            name = line[0]
            url = line[1]
            img_url = line[2]
            break
        line = f2.readline()
    f2.close()

    result['name'] = name
    result['url'] = url
    result['img_url'] = img_url
    result['contained_keywords'] = keywords
    result['query_match'] = similarity[title]
    result['content'] = content

    return result


# 处理查询字符串，返回检索结果
def retrieval_query(input_str):
    # 返回多个结果
    Results = []

    # 筛选关键词
    keywords = seg_sentence(input_str)

    # 创建文档列表
    docu_set = create_docu_set()

    # 存在查询关键词的文档索引
    text_list = get_similar_texts(input_str)
    text_set = set(text_list)
    text_list = list(text_set)

    # 获取各个文档与查询的相关度
    similarity = get_similarity(docu_set, keywords, text_list)
    # 将各文档的相关度按照从大到小排序
    similarity = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=True))

    for k in similarity.keys():
        title = str(k)
        result = get_result(similarity, title, keywords)
        Results.append(result)

    return_pack = {'results': Results, 'origin_input_str': input_str, 'input_str_keywords': keywords}

    return return_pack
