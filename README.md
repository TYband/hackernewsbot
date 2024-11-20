# Hacker News 自动转发与翻译 Bot

这是一个 Python 脚本，自动从 Hacker News 获取热门新闻，翻译新闻标题为中文，并生成 Markdown 文件上传到 GitHub 仓库，方便部署在个人博客上。适合每日新闻分享和自动化发布。

## 功能简介

- **获取 Hacker News 热门新闻**：使用 Hacker News 官方 API 获取每日热门新闻。
- **自动翻译**：通过 `deep_translator` 将新闻标题翻译为中文。
- **生成 Markdown 文件**：按照预设模板生成适合 Jekyll 的 Markdown 文件。
- **自动上传到 GitHub**：利用 `PyGithub` 实现文件的上传或更新。

## 环境依赖

Python 3.7 或更高版本
需要安装以下 Python 库：
  ```
  pip install requests schedule deep-translator PyGithub
  ```
克隆项目：
  ```
git clone git@github.com:TYband/hackernewsbot.git
cd TYband/hackernewsbot
  ```
设置脚本中的配置项： 打开 hack.py，配置以下参数：

GITHUB_REPO：你的 GitHub 仓库名称（格式为 用户名/仓库名）。

GITHUB_TOKEN：你的 GitHub TOKEN。

GITHUB_DIR_PATH：存放 Markdown 文件的目录路径。

运行脚本：
  ```
python hack.py
  ```
定时任务
脚本默认每 3 小时执行一次任务。你可以修改以下代码调整频率：
  ```
schedule.every(3).hours.do(scheduled_task)
  ```
