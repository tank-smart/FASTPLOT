# -*- coding: utf-8 -*-

# =============================================================================
# =======概述
# 创建日期：2018-05-15
# 简述：。。。
#
# =======使用说明
# 。。。
#
# =======日志
# 
# =============================================================================

import re
import sys

#导入包app所在的目录，以便本文件可访问app下的Python模块
#要使普通的文件夹成为Python包需在此文件夹下添加一个__init__.py文件，此文件可以为空
#若不是Python包则无法被Python模块使用
#需要解决自定义包访问的问题，通过改变工作路径
sys.path.append(r"E:\DAGUI\lib")
sys.path.append(r"E:\DAGUI\lib\views")
sys.path.append(r"E:\DAGUI\lib\models")

from app.start import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())