"""当前资料的准备入口，不含目标分析模型。"""
import json
from common import read
from history import histories
def prepare():
    data=read()
    return histories(data,data['asof'])
if __name__=="__main__":print(json.dumps(prepare(),ensure_ascii=False,indent=2))
