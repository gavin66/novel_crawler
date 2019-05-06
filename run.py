# -*- coding: UTF-8 -*-
import sys
import app

# 可调用列表
callable_list = ['search', 'catalog', 'chapter']
if len(sys.argv) < 3 or sys.argv[1] not in callable_list:
    app.error('参数错误')

print(getattr(app, sys.argv[1])(sys.argv[2]))
