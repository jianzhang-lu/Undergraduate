class ListNode:
    def __init__(self, val=0, next=None):
        self.value = val
        self.next = next

    def AddNext(self, nextnode):
        self.next = nextnode

    def __str__(self):
        return str(self.value)


def SwapNodes(head: ListNode):
    # 建立虚拟节点
    dummy = ListNode(-1, head)
    cur = dummy
    while cur.next is not None and cur.next.next is not None:
        temp1 = cur.next
        temp2 = cur.next.next.next
        cur.next = temp1.next
        cur.next.next = temp1
        temp1.next = temp2
        cur = cur.next.next
    return dummy.next


nodes = list(map(int, input().split(", ")))
listnodes = []
for i in range(len(nodes)):
    listnodes.append(ListNode(nodes[i]))
for i in range(len(listnodes)-1):
    listnodes[i].AddNext(listnodes[i+1])
listnodes[-1].AddNext(None)
new_head = SwapNodes(listnodes[0])
result = []
while new_head is not None:
    result.append(new_head.value)
    new_head = new_head.next
print(result)

