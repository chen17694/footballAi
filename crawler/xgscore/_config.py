# -*- coding: utf-8 -*-
"""
内部辅助：把上级目录 ai/ 加进 sys.path，并从 config.py 导入 URL。

供本包内各模块引用，避免每个模块都重复写上级目录路径的处理。
"""

import os
import sys

_PARENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

PREVIEW_URL = ""
XGSCORE_URL = ""
