import os
import requests
import schedule
import time
from datetime import datetime
from googletrans import Translator
from github import Github
import logging

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(), logging.FileHandler("hacknews_bot.log")])

# 配置
HACKERNEWS_API = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
GITHUB_REPO = ""  # 仓库地址
GITHUB_TOKEN = "" # github TOKEN
GITHUB_DIR_PATH = "" # 存放文章 

# 获取当天的时间戳
def get_today_timestamp():
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return int(today_start.timestamp())

# 获取 Hacker News 数据
def get_hacker_news():
    logging.info("正在获取 Hacker News 数据...")
    response = requests.get(HACKERNEWS_API)
    top_ids = response.json()
    news_items = []
    today_timestamp = get_today_timestamp()

    for item_id in top_ids:
        if len(news_items) >= 20:
            break
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json?print=pretty"
        item_response = requests.get(item_url)
        item = item_response.json()
        if item and item.get('time', 0) >= today_timestamp:
            news_items.append({
                "title": item.get("title"),
                "url": f"https://news.ycombinator.com/item?id={item.get('id')}",
                "translation": None
            })

    logging.info(f"成功获取到 {len(news_items)} 条当天的 Hacker News 数据")
    return news_items

# 翻译新闻标题
def translate_news(news_items):
    logging.info("正在翻译新闻标题...")
    translator = Translator()
    for item in news_items:
        item['translation'] = translator.translate(item['title'], src='en', dest='zh-cn').text
    logging.info("新闻标题翻译完成")
    return news_items

# 生成 Markdown 内容，首次创建时包含头部信息
def generate_markdown(news_items, current_date, is_new_file):
    logging.info("正在生成 Markdown 文件内容...")
    header = f'''---
layout: post
title: Hacknews {current_date} 新闻
category: Hacknews
tags: hacknews
keywords: hacknews
coverage: hacknews-banner.jpg
---

Hacker News 是一家关于计算机黑客和创业公司的社会化新闻网站，由保罗·格雷厄姆的创业孵化器 Y Combinator 创建。
与其它社会化新闻网站不同的是 Hacker News 没有踩或反对一条提交新闻的选项（不过评论还是可以被有足够 Karma 的用户投反对票）；只可以赞或是完全不投票。简而言之，Hacker News 允许提交任何可以被理解为“任何满足人们求知欲”的新闻。

## HackNews Hack新闻
''' if is_new_file else ""

    items = ""
    for item in news_items:
        items += f"- [{item['title']}]({item['url']})\n"
        items += f"- {item['translation']}\n"

    markdown_content = header + items
    logging.info("Markdown 文件内容生成完成")
    return markdown_content

# 上传到 GitHub 仓库
def upload_to_github(content, current_date, is_new_file):
    logging.info("正在上传到 GitHub...")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)

    filename = f"{current_date}-hacknews.md"
    file_path = os.path.join(GITHUB_DIR_PATH, filename)

    try:
        file = repo.get_contents(file_path)
        new_content = content  # 仅追加新闻内容
        repo.update_file(file.path, "Update Hacknews post", new_content, file.sha)
        logging.info(f"成功更新 {file_path} 在 GitHub 上")
    except Exception as e:
        repo.create_file(file_path, "Create Hacknews post", content)
        logging.info(f"成功创建 {file_path} 在 GitHub 上")

# 获取当前日期并格式化
def get_current_date():
    return datetime.now().strftime('%Y-%m-%d')

# 定时任务函数
def scheduled_task():
    current_date = get_current_date()
    logging.info(f"任务开始，当前日期是: {current_date}")

    news_items = get_hacker_news()
    news_items = translate_news(news_items)

    # 检查文件是否已经存在
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
    file_path = os.path.join(GITHUB_DIR_PATH, f"{current_date}-hacknews.md")

    try:
        repo.get_contents(file_path)
        is_new_file = False  # 文件已存在
    except Exception:
        is_new_file = True  # 文件不存在，标记为新文件

    markdown_content = generate_markdown(news_items, current_date, is_new_file)
    upload_to_github(markdown_content, current_date, is_new_file)

    logging.info(f"任务完成，{current_date} 的新闻已经上传到 GitHub")

# 主函数
def main():
    schedule.every(3).hours.do(scheduled_task)
    logging.info("脚本已启动，正在等待执行定时任务...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
