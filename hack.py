import os
import requests
import schedule
import time
from datetime import datetime
from deep_translator import GoogleTranslator
from github import Github
import logging

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(), logging.FileHandler("hacknews_bot.log")])

# 配置
HACKERNEWS_API = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
GITHUB_REPO = ""  # 替换为你的 GitHub 仓库 
GITHUB_TOKEN = ""  # 替换为你的 GitHub Token
GITHUB_DIR_PATH = ""  # 存放 Markdown 文件的目录

# 获取 Hacker News 数据
def get_hacker_news():
    logging.info("正在获取 Hacker News 数据...")
    response = requests.get(HACKERNEWS_API)
    top_ids = response.json()
    news_items = []
    for item_id in top_ids[:50]:  # 控制数量以提高效率
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json?print=pretty"
        item_response = requests.get(item_url)
        item = item_response.json()
        if item:
            # 使用 item_id 作为唯一的 id
            news_items.append({
                "id": item_id,
                "title": item.get("title"),
                "url": item.get("url", ""),
                "translation": None
            })
    logging.info(f"成功获取到 {len(news_items)} 条 Hacker News 数据")
    return news_items

# 翻译新闻标题
def translate_news(news_items):
    logging.info("正在翻译新闻标题...")
    for item in news_items:
        try:
            item['translation'] = GoogleTranslator(source='en', target='zh-CN').translate(item['title'])
        except Exception as e:
            logging.error(f"翻译新闻 '{item['title']}' 失败: {e}")
            item['translation'] = "翻译失败"
    logging.info("新闻标题翻译完成")
    return news_items

# 生成 Markdown 内容
def generate_markdown(news_items, current_date):
    logging.info("正在生成 Markdown 文件内容...")
    template = '''---
layout: post
title: Hacknews {date} 新闻
category: Tech News
tags: [Hacker News, Tech News, Programming, Startups, 最新科技新闻]
keywords: [Hacker News, Tech News, Programming, Startups, 最新科技新闻]
coverage: hacknews-banner.jpg
id: {unique_id}
---

Hacker News 是一家关于计算机黑客和创业公司的社会化新闻网站，由保罗·格雷厄姆的创业孵化器 Y Combinator 创建。

## HackNews Hack新闻

{items}
'''

    items = ""
    for item in news_items:
        # 为每个新闻项生成唯一的 id，使用 item_id 或者 url
        unique_id = item['id']  # 可以改为 item['url'] 或其他
        items += f"- [{item['title']}]({item['url']})\n"
        items += f"- {item['translation']}\n"

    markdown_content = template.format(date=current_date, unique_id=unique_id, items=items)
    logging.info("Markdown 文件内容生成完成")
    return markdown_content

# 上传到 GitHub 仓库
def upload_to_github(content, current_date):
    logging.info("正在上传到 GitHub...")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)

    filename = current_date + "-hacknews.md"
    file_path = os.path.join(GITHUB_DIR_PATH, filename)

    try:
        file = repo.get_contents(file_path)
        current_content = file.decoded_content.decode("utf-8")  # 这里定义了 current_content

        # 检查内容是否一致
        if current_content == content:
            logging.info(f"内容与当前内容相同，跳过文件更新：{file_path}")
            # 添加空提交来触发 Pages 重新构建
            repo.create_git_commit("Trigger GitHub Pages rebuild", repo.get_git_commit(repo.get_commits()[0].sha), [])
            logging.info("创建了空提交来触发 GitHub Pages 重新构建")
            return

        # 如果内容不同，则更新文件
        repo.update_file(file.path, "Update Hacknews post", content, file.sha)
        logging.info(f"成功更新 {file_path} 在 GitHub 上")
    except Exception as e:
        logging.error(f"文件更新失败，错误: {e}")
        # 如果文件不存在，创建新文件
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
    markdown_content = generate_markdown(news_items, current_date)
    upload_to_github(markdown_content, current_date)

    logging.info(f"任务完成，{current_date} 的新闻已经上传到 GitHub")

# 主函数
def main():
    # 每3小时执行一次定时任务
    schedule.every(1).minutes.do(scheduled_task)

    # 启动定时任务
    logging.info("脚本已启动，正在等待执行定时任务...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
