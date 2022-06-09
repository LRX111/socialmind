#!/usr/bin/env python 
# -*- coding:utf-8 -*-

class Node():
    # 节点类
    def __init__(self, data=-1):
        self.data = data
        self.left = None
        self.middle = None
        self.right = None


class Tree():
    # 树类
    def __init__(self):
        self.root = Node()

    def add(self, data):
        # 为树加入节点
        node = Node(data)
        if self.root.data == -1:  # 如果树为空，就对根节点赋值
            self.root = node
        else:
            myQueue = []
            treeNode = self.root
            myQueue.append(treeNode)
            while myQueue:  # 对已有的节点进行层次遍历
                treeNode = myQueue.pop(0)
                if not treeNode.left:
                    treeNode.left = node
                    return
                elif not treeNode.middle:
                    treeNode.middle = node
                    return
                elif not treeNode.right:
                    treeNode.right = node
                    return
                else:
                    myQueue.append(treeNode.left)
                    myQueue.append(treeNode.middle)
                    myQueue.append(treeNode.right)

    def DFS_STACK(self, root):  # 基于栈数据结构实现的深度遍历
        if root == None:
            return
        stack = []
        jilu_stack = []
        stack.append(root)
        #count = 0
        while stack:
            now_node = stack.pop()
            jilu_stack.append(now_node.data)

            #print(now_node.data)
            if now_node.right != None:
                stack.append(now_node.right)
            if now_node.middle != None:
                stack.append(now_node.middle)
            if now_node.left != None:
                stack.append(now_node.left)
            else:
                print(jilu_stack)
                jilu_stack.pop()


if __name__ == '__main__':
    # 主函数
    datas = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    tree = Tree()  # 新建一个树对象
    for data in datas:
        tree.add(data)  # 逐个加入树的节点

    print('基于栈数据结构实现的深度遍历：')
    tree.DFS_STACK(tree.root)