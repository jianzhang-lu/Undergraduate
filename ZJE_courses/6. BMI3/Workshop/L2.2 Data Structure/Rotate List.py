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
length = len(nodes)
head = ListNode(nodes[0])
dummy_head = head
for node in nodes[1:]:
    head.AddNext(ListNode(node))
    head = head.next


def rotate(head: ListNode, num: int, length: int):
    dummy_head = head
    dummy_head2 = head
    while head.next:
        head = head.next
    end_node = head

    move = num % length
    count = 0
    if move == 0:
        return dummy_head
    else:
        start = dummy_head
        while count < move-1:
            start = start.next
            count += 1
        res_start = start.next
        start.next = None
        end_node.next = dummy_head2
    return res_start


res = rotate(dummy_head, 6, length)
res_list = [res.val]
while res.next:
    res_list.append(res.next.val)
    res = res.next
print(res_list)