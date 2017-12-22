# -*- coding: utf-8 -*-
# @Author: k
# @Date:   12/20/2017 3:36 PM
"""
This is a raw version of a hash map written in Python. But the implementation is in Java's strategy including hash code
function, bucket index calculation and resizing routine. This strategy distributes the key-value pair in the hash map
evenly, avoids collision very well and reduces resizing workload a lot. There still many things to explore and refine
in this very important data structure.
"""


class MyHashMap:
    """
    My hash sap which supports resizing implemented with arrays and linked lists.
    """
    def __init__(self, capacity=8, load_factor=0.75):
        """
        Initial function of my hash map.
        :param capacity: The capacity (bucket numbers) of the hash map, default is 8. When the occupation of buckets
        exceeds current capacity * load_factor, the capacity * 2. The capacity is always 2's power.
        :param load_factor: Decide when we expand the hash map's capacity, default is 0.75.
        """
        self.capacity = capacity
        self.load_factor = load_factor
        # the hash map's size, i.e. the number of key value pairs stored in the hash map
        self.size = 0
        # the number of occupied buckets
        self.occupation = 0
        # initialize the buckets (array) with length of capacity
        self.buckets = [None] * self.capacity

    @staticmethod
    def _hash(key):
        """
        Calculate the keys's hash code for our hash map.
        :param key: The key.
        :return: (int) The hash code of the key for our hash map.
        """
        # get the origin hash code by build-in hash function
        h = hash(key)
        # generate our hash code by XOR the higher 16 bits and lower 16 bits of origin hash code
        # we use it to define the index of bucket to put this K-V pair
        return h ^ (h >> 16)

    def _index(self, hash_code):
        """
        Extract the lower part of hash_code to decide which bucket to put.
        Because capacity is always 2's power, capacity - 1 will be all 1 in binary format.
        :param hash_code: The hash code of the key.
        :return: (int) The index of the bucket.
        """
        return hash_code & (self.capacity - 1)

    def put(self, key, val):
        """
        Put the K-V pair's node to our hash map.
        :param key: The key.
        :param val: The key's value.
        """
        # if the hash map already contains the key, get the node and update it's value directly
        if self.__contains__(key):
            self._get_node(key).val = val
            return
        # check if the occupation exceed the threshold to resize the hash map, if it needs, resize it first
        if self.occupation >= self.capacity * self.load_factor:
            self._resize()
        # calculate the hash code
        hash_code = self._hash(key)
        # calculate the bucket index
        idx = self._index(hash_code)
        # if there's a collision, put the node to the tail of this linked list
        if self.buckets[idx]:
            cur = self.buckets[idx]
            while cur.next:
                cur = cur.next
            cur.next = ListNode(hash_code, key, val)
        # else put the node in the bucket directly
        else:
            self.buckets[idx] = ListNode(hash_code, key, val)
            # update occupation
            self.occupation += 1
        # update size
        self.size += 1

    def get(self, key):
        """
        Get a key's value, if this key doesn't exist in the hash map, raise a KeyError.
        :param key: The key.
        :return: The key's value.
        """
        return self._get_node(key).val

    def _get_node(self, key):
        """
        Get the node of the corresponding key, if the node doesn't exist in the hash map, raise a KeyError.
        :param key: The key.
        :return: (ListNode) The node of the key.
        """
        hash_code = self._hash(key)
        idx = self._index(hash_code)
        # extract the head of the corresponding bucket
        cur = self.buckets[idx]
        while cur:
            if cur.key == key:
                return cur
            cur = cur.next
        raise KeyError

    def _resize(self):
        """
        Resize the hash map.
        """
        # double the buckets number
        self.buckets.extend([None] * self.capacity)
        self.capacity *= 2
        # check each node in our hash map, if a node needs to move to a new bucket, we call _move function
        for idx in range(self.capacity // 2):
            cur = self.buckets[idx]
            # a symbol denotes that if current node is a linked list's head
            list_head = True
            while cur:
                # if the node need to process is a head node, we process it (current node)
                if list_head:
                    hash_code = cur.hash
                    new_idx = self._index(hash_code)
                    # if the new index doesn't equal to old index, we need move it
                    if new_idx != idx:
                        self._move(cur, idx, new_idx, list_head)
                        cur = self.buckets[idx]
                        continue
                    # else we don't need to process the head node, so we change the list_head symbol
                    else:
                        list_head = False
                # else if the node (cur's next) need to process is not a head node, we process current node's next
                elif cur.next:
                    hash_code = cur.next.hash
                    new_idx = self._index(hash_code)
                    # if the new index doesn't equal to old index, we need move it
                    if new_idx != idx:
                        self._move(cur, idx, new_idx, list_head)
                    else:
                        cur = cur.next
                else:
                    cur = cur.next

    def _move(self, node, old_idx, new_idx, list_head):
        """
        Move a node from old bucket to new bucket.
        :param node: The current node.
        :param old_idx: Old bucket's index.
        :param new_idx: New bucket's index.
        :param list_head: A symbol denotes if current node is a head node of a linked list.
        """
        # if the node is a head node
        if list_head:
            # we process current node
            move_node = node
            # change the old bucket's head to its next node
            self.buckets[old_idx] = move_node.next
            # if the node's next in None means this bucket become empty, so occupation - 1
            if not move_node.next:
                self.occupation -= 1
        # if the node is not a head node, we process current node's next node
        else:
            move_node = node.next
            node.next = move_node.next
        # change the moved node's next to None
        move_node.next = None
        # move the move to new bucket
        if self.buckets[new_idx]:
            cur = self.buckets[new_idx]
            while cur.next:
                cur = cur.next
            cur.next = move_node
        # if the new bucket is empty, occupation + 1
        else:
            self.buckets[new_idx] = move_node
            self.occupation += 1

    def __contains__(self, key):
        """
        Support checking if a key in the hash map, if not raise a KeyError.
        :param key: The key
        :return: (bool) True of False
        """
        try:
            self._get_node(key)
            return True
        except KeyError:
            return False

    def __setitem__(self, key, val):
        """
        Support putting K-V pair in the hash map in "dict[key] = value" format.
        """
        return self.put(key, val)

    def __getitem__(self, key):
        """
        Support getting value in the hash map in "dict[key]" format.
        """
        return self.get(key)

    def __len__(self):
        """
        Support getting the size of the hash map in "len(hash_map)" format.
        """
        return self.size


class ListNode:
    """
    The node to store a k-v pair.
    """
    def __init__(self, hash, key, val):
        """
        Initial function of the list node.
        :param hash: The key's hash code.
        :param key: The key.
        :param val: The value.
        """
        self.hash = hash
        self.key = key
        self.val = val
        # Initialize the node's next as None.
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
