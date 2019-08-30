leet-code最热100题
==================

两数之和
--------
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标
``解题思路：有点像两个骰子之和哈，只不过不能有index不能是自己。可以分为x轴和y轴的和，为了避免重复计算，以
x轴为遍历基础，y轴的值在index为len(l)-x中寻找。``

.. code:: python
    def get_two_sum(l, goal):
        for i, v in enumerate(l):
            for i2, v2 in enumerate(l[i+1:]):
                if goal == v + v2:
                    return (i, i+1+i2)

    # test
    l = [random.randint(1,10) for x in range(10)]
    goal = random.randint(10/2,10*2)
    print(get_two_sum(l, goal))


费控证书链表求和
----------------
给出两个 非空 的链表用来表示两个非负的整数。其中，它们各自的位数是按照 逆序 的方式存储的，并且它们的每个节点只能存储 一位 数字。
如果，我们将这两个数相加起来，则会返回一个新的链表来表示它们的和
``解题思路：首先链表是左对齐的，当长度不一样的时候，可以将多出的部分截断补充到结果后。
当低位（左1）节点相加大于9则进1，也就是下一个节点值+1``

.. code:: python
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
    # 题后说明，其实处理链表这个东西用栈是最合适不过了, python用list


无重复字符的最长子串
--------------------
给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。
``解题思路：分段记录不重复子串，出现重复字符则分段处理``

.. code:: python
    def get_sub_str_not_repeat(s):
        most = 0
        ss = ''
        for v in s:
            if ss.count(v):
                if most < len(ss):
                    most = len(ss)
                ss = v
            else:
                ss += v
        return most

求两个有序数列的中位数
----------------------
给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。
请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))
``单个数列的中位数分奇偶，两个数列的中位数先要合并俩数列再当做单数列求中位数
但是这样复杂度要求肯定是不到log(m+n)了，只是O(m+n), 要到log级，就需要采取二分法``

.. code:: python
    
