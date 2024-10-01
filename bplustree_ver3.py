class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BPlusTree:
    def __init__(self, t):
        self.root = BPlusTreeNode(True)
        self.t = t

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BPlusTreeNode()
            self.root = temp
            temp.children.append(root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, key)
        else:
            self.insert_non_full(root, key)

    def insert_non_full(self, node, key):
        if node.leaf:
            node.keys.append(key)
            node.keys.sort()
        else:
            i = len(node.keys) - 1
            while i &gt;= 0 and key &lt; node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split_child(node, i)
                if key &gt; node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], key)

    def split_child(self, parent, index):
        t = self.t
        child = parent.children[index]
        new_child = BPlusTreeNode(child.leaf)
        parent.keys.insert(index, child.keys[t-1])
        parent.children.insert(index + 1, new_child)
        new_child.keys = child.keys[t:(2*t) - 1]
        child.keys = child.keys[0:t-1]
        if not child.leaf:
            new_child.children = child.children[t:2*t]
            child.children = child.children[0:t]

    def in_order_traversal(self):
        if self.root is not None:
            return self._in_order_traversal(self.root)

    def _in_order_traversal(self, node):
        keys = []
        if node.leaf:
            return node.keys
        for i, key in enumerate(node.keys):
            keys.extend(self._in_order_traversal(node.children[i]))
            keys.append(key)
        keys.extend(self._in_order_traversal(node.children[-1]))
        return keys

# Example usage
bpt = BPlusTree(3)
keys = [10, 20, 5, 6, 12, 30, 7, 17]
for key in keys:
    bpt.insert(key)

print("In-order traversal of the B+ Tree:")
print(bpt.in_order_traversal())