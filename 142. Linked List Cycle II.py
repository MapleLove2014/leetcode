# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        nodes = set()
        node = head
        while node:
            if node in nodes:
                return node
            nodes.add(node)
            node = node.next
        return node

    def floyd(self, head: ListNode) -> ListNode:
        hare = head
        tortoise = head
        hasLoop = False
        while hare and hare.next:
            hare = hare.next.next
            tortoise =tortoise.next
            if hare == tortoise:
                hasLoop = True
                break
        if not hasLoop:
            return None
        node = head
        while node != tortoise:
            node = node.next
            tortoise = tortoise.next
        return node