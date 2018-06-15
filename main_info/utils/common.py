# 问句天几高，心中志比天更高
# 自定义模板过滤器
def do_index_filter(index):
    if index == 1:
        return 'first'
    elif index == 2:
        return 'second'
    elif index == 3:
        return 'third'
    else:
        return ''
