import crawler_modules
import re
import asyncio
## app
async def main():
    for number in range(11930, 100001):
        url = f"https://drugs.dxy.cn/baidu/aspirin/find_drugs.htm?drugId={number}"
        docs = await crawler_modules.playwright_crawler_async(url)
        doc = docs[0].page_content
        new_string = re.sub('[\n丁香医生,\n>Home\n]', '', doc)
        t_len = len(new_string)
        # 写入文本文件
        if t_len == 34 or t_len == 454:
            print(f"pass:{number}")
            pass
        else:
            with open(f'docs/drugs_{number}.txt', 'w') as file:
                file.write(new_string)
                print(f"docs:{number}")
# if __name__ == "__main__":
#     main()
# Python 3.7+
asyncio.run(main())