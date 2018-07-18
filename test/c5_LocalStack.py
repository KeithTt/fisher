from werkzeug.local import LocalStack

# push、pop、top

# 实例化一个对象
s = LocalStack()

# 把一个元素推入到栈顶
s.push(1)

# 读取栈顶元素、top是一个属性
print(s.top)
print(s.top)

# 弹出栈顶元素、pop是一个方法
print(s.pop())
print(s.top)

# 推入两个元素
s.push(1)
s.push(2)

# 栈 后进先出
print(s.top)
print(s.top)
print(s.pop())
print(s.top)

# 2
# 2
# 2
# 1
