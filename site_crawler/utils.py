import re
import hashlib


def get_md5(value):
    m = hashlib.md5()
    m.update(str(value).encode("utf-8"))
    return m.hexdigest()


def get_category_by_biquge(value):
    match_obj = re.match(r'.*?>(.*)?>.*', value)
    if match_obj:
        return match_obj.group(1).strip()
    else:
        return ""


def get_author_by_biquge(value):
    match_obj = re.match(r'^作.*?者：(\w+)', value)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""
