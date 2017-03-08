from ast import parse
arg1 = [1,2,3,4]
arg2 = [5,6,7,8]
code = """
ret = []

arg3 = []
arg4 = []

for i1 in arg1:
    pass

for i2 in arg2:
    pass
    
print i1, i2
"""

node = parse(code)
exec compile(node, '<string>', 'exec')
print "-"*64


for1 = node.body[3]
print for1.body.pop()
for2 = node.body[4]
for1.body.append(for2)
del node.body[4]
for2.body.pop()
for2.body.append(node.body[4])


exec compile(node, '<string>', 'exec')