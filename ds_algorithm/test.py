print('# 两数之和 #')
print('-------------------------------------------')
import random
def get_two_sum(l, goal):
    for i, v in enumerate(l):
        for i2, v2 in enumerate(l[i+1:]):
            if goal == v + v2:
                return (i, i+1+i2)

# test
l = [random.randint(1,10) for x in range(10)]
goal = random.randint(10/2,10*2)
print('[给定数组]', l)
print('[目标和值]', goal)
print('[输出] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
print(get_two_sum(l, goal))

print()
print('# 链表相加求和 #')
print('-------------------------------------------')
# 先构造节点
class Node:
    def __init__(self, v=0):
        self.val = v
        self.next = None
    def __repr__(self):
        p = '->'
        ps = ''
        while self and self.val >= 0:
            ps += str(self.val)
            if self.next:
                ps += p
            self = self.next
        return ps

def list2LNode(l):
    '''用于转化l为LNode'''
    tmpL = []
    for v in l:
        if v >= 0:
            node = Node(v)
            node.val = v
            tmpL.append(node)
        else:
            raise ValueError('value of list cant < 0')

    # to ->
    last = tmpL[0]
    for v in tmpL[1:]:
        last.next = v
        last = v
    return tmpL[0]

# test Node
l1 = [1,5,6,2,5,2,3,5,7]
l2 = [3,4,6,1,3]
ln1 = list2LNode(l1)
ln2 = list2LNode(l2)
print('[ln1] ', l1)
print('[node ln1] ', ln1)
print('[ln2] ', l2)
print('[node ln2] ', ln2)

def sumLNode(ln1, ln2):
    up = 0
    last = Node(-1)
    while (ln1 or ln2):
        node = Node(0)

        # get first node
        if last.val == -1:
            print(node.val)
            first = node

        # cal
        if ln1 and ln2:
            # 两者都有值
            v = ln1.val + ln2.val + up
            if v > 9:
                node.val = v % 10
                up = 1
            else:
                node.val = v
                up = 0
            ln1 = ln1.next
            ln2 = ln2.next
            last.next = node
            last = node
        elif ln1:
            # ln1 还存在值 ln2=None , 截断ln1
            ln1.val += up
            last.next = ln1
            ln1 = None
        elif ln2:
            ln2.val += up
            last.next = ln2
            ln2 = None
        
    return first
            
# test sumNode
suml = sumLNode(ln1, ln2)
print('[输出] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
print('[suml] ', suml)

            
print('# 无重复子串 #')
print('-------------------------------------------')
s = 'dshfioaipoadjpqhdcdqucncovhnxzl'
def get_sub_str_not_repeat(s):
    l = []
    ss = ''
    for v in s:
        if ss.count(v):
            l.append((ss,len(ss)))
            ss = v
        else:
            ss += v
    if ss:
        l.append((ss,len(ss)))
    print(l)
    max_t = ('',0)
    for v in l:
        if v[1] > max_t[1]:
            max_t = v
    return max_t
print('[s] ', s)
print('[输出] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
print('[max_t] ', get_sub_str_not_repeat(s))
def get_sub_str_not_repeat2(s):
    most = 0
    ss = ''
    for v in s:
        if ss.count(v):
            if most < len(ss):
                most = len(ss)
            ss = v
        else:
            ss += v
    if ss and most < len(ss): most = len(ss) 
    return most
print('[sub2]', get_sub_str_not_repeat2(s))

print('# 两个有序数组的中位数 #')
print('-------------------------------------------')
def get_middle_by_order_arr(l1, l2):
    # 合并两个有序数组
    l3 = l1 + l2
    
