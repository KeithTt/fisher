# 爬虫，scrapy，requests + beautiful soup

import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        # restful -> json
        if r.status_code == 200:
            if return_json:
                return r.json()
            else:
                return r.text
        else:
            if return_json:
                return {}
            else:
                return ''
        # 三元表达式简化if/else
        # if r.status_codes() != 200:
        #     return {} if return_json else ''
        # return r.json() if return_json else r.text
