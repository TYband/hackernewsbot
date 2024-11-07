Hacker News 自动推送脚本
项目简介
该项目是一个自动化脚本，用于定时获取 Hacker News 当日热门新闻并推送至指定的 GitHub 仓库。通过 GitHub Actions 或本地调度，该脚本会每 3 小时从 Hacker News 获取最新的热门新闻，自动翻译成中文，并生成 Markdown 格式的新闻更新文件。如果当天文件尚不存在，它会创建一个带头部信息的文件；如果已存在，则仅更新内容部分。适合搭建个人博客每日新闻推送等应用。

功能说明
定时获取 Hacker News 热门新闻：每 3 小时运行一次，获取最新 20 条当天新闻。
标题自动翻译：使用 Google 翻译 API 将英文标题翻译为中文。
Markdown 文件生成：如果是当天首次创建文件，生成包含头部信息的 Markdown 文件；否则，仅追加新闻内容。
自动推送到 GitHub：将更新的文件推送至 GitHub 仓库，可用于静态博客每日新闻更新。
使用指南
配置 GitHub 仓库：在 GITHUB_REPO 中设置你要推送到的 GitHub 仓库地址（如 username/repository）。
配置 GitHub Token：在 GITHUB_TOKEN 中填入你的 GitHub 访问令牌，确保有写入权限。
安装依赖：
```
pip install requests schedule googletrans==4.0.0-rc1 PyGithub
```
运行脚本：
```
python hacknews_bot.py
```
或将该脚本设置为系统服务，以便后台运行。
项目依赖
requests：用于发起 HTTP 请求以获取 Hacker News 数据。
schedule：用于设置定时任务。
googletrans：用于将新闻标题从英文翻译为中文。
PyGithub：用于操作 GitHub API 推送内容。
主要代码逻辑
get_hacker_news()：调用 Hacker News API 获取最新新闻数据。
translate_news()：使用 Google 翻译 API 将新闻标题翻译成中文。
generate_markdown()：生成或追加 Markdown 文件内容。
upload_to_github()：检查是否存在当天文件，并根据情况进行创建或更新。
注意事项
Google Translate：请确保 Google Translate API 未被墙，或使用合适的代理。
GitHub Token 权限：GitHub 访问令牌应具有推送权限。
运行频率：默认每 3 小时运行一次，如需调整，可在 schedule.every(3).hours 修改频率。
日志记录
所有的任务执行、获取新闻数据、翻译和推送更新均会记录在日志文件 hacknews_bot.log 中，以便调试和记录执行情况。

示例
生成的 Markdown 文件样例如下：


---
layout: post
title: Hacknews 2024-11-07 新闻
category: Hacknews
tags: hacknews
keywords: hacknews
coverage: hacknews-banner.jpg
---

Hacker News 是一家关于计算机黑客和创业公司的社会化新闻网站，由保罗·格雷厄姆的创业孵化器 Y Combinator 创建。
与其它社会化新闻网站不同的是 Hacker News 没有踩或反对一条提交新闻的选项（不过评论还是可以被有足够 Karma 的用户投反对票）；只可以赞或是完全不投票。简而言之，Hacker News 允许提交任何可以被理解为“任何满足人们求知欲”的新闻。

## HackNews Hack新闻

- [Sample News Title](https://news.ycombinator.com/item?id=123456)
- 样例新闻标题
