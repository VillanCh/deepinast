import ast

forcode_tmp = """
for {valuebase}{index} in {iterbase}{index}:
    pass
"""

yieldcode_tmp = """
yield tuple([{content}])
"""

define_tmp = """
{iterbase}{index} = args[{index}]
"""

func_tmp = """
def func(*args):
    pass
"""

#----------------------------------------------------------------------
def _render_for(iter_id_base, value_id_base, index, filled_expr=None):
    """"""
    iter_id_base = str(iter_id_base)
    value_id_base = str(value_id_base)
    index = int(index)
    
    _tmp = forcode_tmp.format(valuebase=value_id_base,
                              index=index,
                              iterbase=iter_id_base)
    
    _for = ast.parse(_tmp).body.pop()
    
    if filled_expr:
        _for.body.pop()
        _for.body.append(filled_expr)
    
    return _for
    

#----------------------------------------------------------------------
def _render_yield(base, length):
    """"""
    base = str(base)
    length = int(length)
    ret = []
    for i in range(length):
        ret.append((base + '{}').format(i))
    yieldcode_new = yieldcode_tmp.format(content=','.join(ret))
    print yieldcode_new
    return ast.parse(yieldcode_new).body.pop()

#
# section2 yield
#----------------------------------------------------------------------
def _render_core_block(iter_namebase, value_namebase, iter_num):
    """"""
    last = None
    for i in range(iter_num):
        if last == None:
            last = _render_for('iter_', 'n_', i, _render_yield(value_namebase, iter_num))
        else:
            last = _render_for('iter_', 'n_', i, last)
    
    return last

#
# section1 define
#----------------------------------------------------------------------
def _define_iter(iterbase, *args):
    """"""
    defnieblock = []
    for i in range(len(args)):
        define_new = define_tmp.format(index=i, iterbase=iterbase)
        definebody = ast.parse(define_new).body.pop()
        defnieblock.append(definebody)
    
    return defnieblock

#----------------------------------------------------------------------
def iter_remix(*args):
    pass


#----------------------------------------------------------------------
def test():
    """"""
    ret = []
    for i in range(4):
        ret.append(i)
        for j in range(5):
            ret.append(j)
            yield tuple(ret)
            ret.pop()
        ret.pop()
    
for i in test():
    print i


print _render_core_block(iter_namebase='iter_', value_namebase='i_', iter_num=4)
print _define_iter('base_', range(5), range(5,7), range(77))
print iter_remix(range(4), range(6))