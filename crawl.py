from bs4 import BeautifulSoup
import requests

def crawler(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        text = text.strip().replace('\n', '').replace('\t', '')
        if not text:
            text = "程序提示：该网页内容无法读取或内容为空"
        else:
            pass
    else:
        text = f"获取网页失败，状态码：{response.status_code}"
    return text

if __name__ == "__main__":
    url = ""
    if url:
        text = crawler(url)
    else:
        text = "请输入网址"
    print(text)