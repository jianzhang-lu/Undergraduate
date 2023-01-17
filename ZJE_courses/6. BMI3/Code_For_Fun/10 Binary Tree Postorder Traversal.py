class node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def get_value(self):
        return self.val

    def traverse(self):
        result = []

        def post(root):
            if root is None:
                return
            post(root.left)
            post(root.right)
            result.append(root.val)
        post(self)
        return result

    def insert(self, val_list):
        try:
            for val in val_list:
                if not self.val:
                    self.val = val
                elif val < self.val:
                    if self.left == None:
                        self.left = node(None)
                    self.left.insert(val)
                elif val > self.val:
                    if self.right == None:
                        self.right = node(None)
                    self.right.insert(val)
        except TypeError:
            val = val_list
            if not self.val:
                self.val = val
            elif val < self.val:
                if self.left == None:
                    self.left = node(None)
                self.left.insert(val)
            elif val > self.val:
                if self.right == None:
                    self.right = node(None)
                self.right.insert(val)
        return self.traverse()


l = list(map(int, input().split(", ")))
print(node(l[0]).insert(l[1:]))
