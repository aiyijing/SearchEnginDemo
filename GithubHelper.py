import requests
from lxml import etree
# Gitub issues url
url_format = "https://github.com/{}/issues"

# HTTP1.1 Headers
headers = {"User-Agent":
               "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
            "Accept" :
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
           }

# all issues xpath
issues_xpath = '//*[@class="link-gray-dark v-align-middle no-underline h4 js-navigation-open"]/text()'

# Text file write path
data_path = "./data/"


'''
下载指定代码仓库的issue
@:param 仓库名称
@:return issue text
'''
def fetch(name):
    print("download {}".format(name))
    url = url_format.format(name)
    try:
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.text)
        '''
        提取html数据
        '''
        issues = html.xpath(issues_xpath)
        file_path = data_path+name.replace('/', '_')+".txt"
        with open(file_path, 'w') as f:
            for issue in issues:
                f.write(issue+'\n')
            f.close()
        print("done")
    except Exception as e:
        print(e)


'''
读取本地文件
@:param 仓库名称
@:return issue text
'''
def readFile(name):
    path = data_path+name.replace('/', '_')+".txt"
    with open(path, 'r') as f:
        return f.read()

