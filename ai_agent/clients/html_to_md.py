import requests
from markdownify import markdownify as md


class HTMLToMDConverter:
    def convert(self, html):
        return md.convert(html)

    def download_and_convert(self, url, file_name):
        response = requests.get(url)
        html_content = response.text

        markdown_content = md(html_content)

        with open(file_name, "w", encoding="utf-8") as file:
            file.write(markdown_content)
