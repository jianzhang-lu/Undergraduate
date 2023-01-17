# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def insert(self, val: int):
        if self is None:
            self = TreeNode(val)
        # 插入值如果小于node本身的值，则一定在node左侧
        elif val < self.val:
            # 如果node左侧没有节点，则直接插入
            if self.left is None:
                self.left = TreeNode(val)
            # 如果node左侧有节点，则循环此过程再判断
            else:
                self.left.insert(val)

        # 插入值如果大于node本身的值，则一定在node右侧
        else:
            if self.right is None:
                self.right = TreeNode(val)
            else:
                self.right.insert(val)

    def inorderTraversal(self):
        result = []

        def inorder_(root: TreeNode):
            if root is None:
                return
            inorder_(root.left)
            result.append(root.val)
            inorder_(root.right)
        inorder_(self)
        return result


integers = list(map(int, input().split(", ")))
def treeSort(lst: list) -> list:
    # returns a sorted list
    root = TreeNode(integers[0])
    for val in lst[1:]:
        root.insert(val)
    return root.inorderTraversal()


print(treeSort(integers))
