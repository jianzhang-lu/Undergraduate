class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def AddNext(self, nextnode):
        self.next = nextnode

    def __str__(self):
        return str(self.val)


# 建立新的listnodes
# nodes = list(map(int, input().split(", ")))
nodes = [9, 4, 3, 2, 5, 2]
head = ListNode(nodes[0])
dummy_head = head
for node in nodes[1:]:
    head.AddNext(ListNode(node))
    head = head.next


def partition(head: ListNode, x: int) -> ListNode:
    less = ListNode(-1)
    larger = ListNode(-1)
    dummy_less = less
    dummy_larger = larger
    while head:
        if head.val <= x:
            less.next = head
            less = less.next
        else:
            larger.next = head
            larger = larger.next
        head = head.next
    larger.next = None
    less.next = dummy_larger.next
    return dummy_less.next


res = partition(dummy_head, 3)
res_list = [res.val]
while res.next:
    res_list.append(res.next.val)
    res = res.next
print(res_list)




