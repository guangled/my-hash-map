# -*- coding: utf-8 -*-
# @Author: k
# @Date:   12/20/2017 3:36 PM


class MyHashMap:
    def __init__(self, capacity=8, load_factor=0.75):
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [None] * self.capacity

    @staticmethod
    def _hash(key):
        h = hash(key)
        return h ^ (h >> 16)

    def _index(self, hash_code):
        return hash_code & (self.capacity - 1)

    def put(self, key, val):
        if self.__contains__(key):
            self._get_node(key).val = val
            return
        if self.size >= self.capacity * self.load_factor:
            self._resize()
        hash_code = self._hash(key)
        idx = self._index(hash_code)
        if self.buckets[idx]:
            cur = self.buckets[idx]
            while cur.next:
                cur = cur.next
            cur.next = ListNode(hash_code, key, val)
        else:
            self.buckets[idx] = ListNode(hash_code, key, val)
        self.size += 1

    def get(self, key):
        return self._get_node(key).val

    def _get_node(self, key):
        hash_code = self._hash(key)
        idx = self._index(hash_code)
        cur = self.buckets[idx]
        while cur:
            if cur.key == key:
                return cur
            cur = cur.next
        raise KeyError

    def _resize(self):
        self.buckets.extend([None] * self.capacity)
        self.capacity *= 2
        for idx in range(self.capacity // 2):
            cur = self.buckets[idx]
            list_head = True
            while cur:
                if list_head:
                    hash_code = cur.hash
                    new_idx = self._index(hash_code)
                    if new_idx != idx:
                        self._move(cur, idx, new_idx, list_head)
                        cur = self.buckets[idx]
                        continue
                    else:
                        list_head = False
                elif cur.next:
                    hash_code = cur.next.hash
                    new_idx = self._index(hash_code)
                    if new_idx != idx:
                        self._move(cur, idx, new_idx, list_head)
                    else:
                        cur = cur.next
                else:
                    cur = cur.next

    def _move(self, node, old_idx, new_idx, list_head):
        if list_head:
            move_node = node
            self.buckets[old_idx] = move_node.next
        else:
            move_node = node.next
            node.next = move_node.next

        move_node.next = None
        if self.buckets[new_idx]:
            cur = self.buckets[new_idx]
            while cur.next:
                cur = cur.next
            cur.next = move_node
        else:
            self.buckets[new_idx] = move_node

    def __contains__(self, key):
        try:
            self._get_node(key)
            return True
        except KeyError:
            return False

    def __setitem__(self, key, val):
        return self.put(key, val)

    def __getitem__(self, key):
        return self.get(key)

    def __len__(self):
        return self.size


class ListNode:
    def __init__(self, hash, key, val):
        self.hash = hash
        self.key = key
        self.val = val
        self.next = None


if __name__ == '__main__':
    hash_map = MyHashMap()
    ret1, ret2 = [], []
    for i in range(100000):
        hash_map[str(i)] = str(i + 30)
    for i in range(100000):
        ret1.append(hash_map[str(i)])
    for i in range(100000):
        hash_map[str(i)] = i * 2
    for i in range(100000):
        ret2.append(hash_map[str(i)])
    hash_map['abcd'] = 'dcba'

    print(ret1)
    print(ret2)
    print(0 in hash_map, '1' in hash_map)
    print(hash_map['abcd'])
    print(len(hash_map))
