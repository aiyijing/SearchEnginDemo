from GithubHelper import fetch, readFile
import jieba
from collections import Counter
from collections import defaultdict
from prettytable import PrettyTable
#
filter_character = [""]

'''
'''
def char_filter(text):
    for char in filter_character:
        text = text.replace(char, " ")
    return text


'''
从repositoryList读取仓库列表,下载这些数据
@:param null
@:return repositories
'''
def init():
    with open("./repositoryList.txt", 'r') as f:
        repositories = [repository for repository in f.read().split()]
    for repository in repositories:
        fetch(repository)
    return repositories


'''
创建一个倒排索引用defaultdic
@:param repositories list
@:return defaultdic
'''
def create_reverse_index(repositories):
    reverse_index_dic = defaultdict(dict)
    for id in range(0, len(repositories)):

        text = readFile(repositories[id])
        text = char_filter(text)

        words = jieba.cut(text)
        words_count = Counter(words)
        for key in words_count:
            reverse_index_dic[key.lower()][id] = words_count[key]

    return reverse_index_dic

def match_score(match_dic):
    score = {}
    total = 0.0
    for var in match_dic.values():
        total += var

    if total == 0:
        return score
    for key in match_dic.keys():
        score[key] = match_dic[key]/total
    score = sorted(score.items(), key=lambda x: x[1], reverse=True)
    result_dic = {}
    for item in score:
        result_dic[item[0]] = item[1]
    return result_dic

def search(reverse_index_dic,repositories):
    print("Simple search engine(Ctrl+C to quit)")
    while True:
        print("********************************")
        word = input("Please Search Keyword:")
        word = word.lower()

        score = match_score(reverse_index_dic[word])


        if len(score) == 0:
            print("\n")
            print("\tNo matching data")
            print("\n")
        else:
            # use PrettyTable print
            ptable = PrettyTable(["Score", "Repositoriy"])
            for key in score.keys():
                ptable.add_row([score[key], repositories[key]])
            print(ptable)

if __name__=="__main__":
    #初始化文件,从github下载数据
    repositories = init()
    #创建索引
    reverse_index_dic = create_reverse_index(repositories)
    #进行搜索
    search(reverse_index_dic, repositories)
