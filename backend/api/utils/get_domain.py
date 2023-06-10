
from urllib.parse import urlparse
import re


def get_domain(val: str):

    url = val.replace(' ','')

    _url = urlparse(url)

    # 匹配字符串开头
    match = re.match(r"http", url)



    # print(_url)

    if bool(match):
        __a = _url.netloc.split('.')
        if len(__a) == 2:
            return _url.netloc
        else:
            _a = '.'.join(__a[-2:])
        return _a

    else:
        # 传入的不是 http 开头的地址
        if _url.netloc == '' and _url.path != '' and '.' in _url.path: # 如果获取的域名为空
            if "/" in _url.path: # 判断是否有 / 后缀路径
                _b = '.'.join(_url.path.split('/')[:1])

                # 判断是顶级域名，还是二级域，还是三级。等等
                if _b.count('.') == 1:
                    return _b
                else:
                    _c = '.'.join(_b.split('.')[-2:])
                    return _c
            else:

                _b = '.'.join(_url.path.split('/')[:1])
                # 判断是顶级域名，还是二级域，还是三级。等等
                if _b.count('.') == 1:
                    return _b
                else:
                    _c = '.'.join(_b.split('.')[-2:])
                    return _c

        else:
            return url
                