"""Module to implement binary search tree.

Inspired from:
http://interactivepython.org/runestone/static/pythonds/Trees/SearchTreeImplementation.html.

The tutorial explains the implementation of a binary search tree. The following code
has small adjustments, specifically in the insertion of nodes, where duplicate keys
are also handled.

"""


class BinarySearchTree:
    """Binary Search Tree.

    Attributes:
        root (TreeNode): root node.
        size (int): number of nodes in tree.

    """

    def __init__(self):
        """Constructor."""
        self.root = None
        self.size = 0

    def length(self):
        """Size of tree.

        Returns:
            (int): number of nodes in tree.

        """
        return self.size

    def __len__(self):
        """Size of tree.

        Returns:
            (int): number of nodes in tree.

        """
        return self.size

    def __iter__(self):
        """Iterate.

        Returns:
            (Iterator): iterator to go through nodes.

        """
        return self.root.__iter__()

    def __setitem__(self, key, value):
        """Add node.

        Args:
            key (any): key of node.
            value (any): value at node.

        """
        self.put(key, value)

    def __getitem__(self, key):
        """Get node.

        Args:
            key (any): key of node.

        Returns:
            (any): value at node.

        """
        return self.get(key)

    def __contains__(self, key):
        """Overload "in" operator.

        Args:
            key (any): key of node.

        Returns:
            (bool): flag if node with key exists in tree.

        """
        if self._get(key, self.root):
            return True
        else:
            return False

    def __delitem__(self, key):
        """Call delete (del).

        Args:
            key (any): key of node.

        """
        self.delete(key)

    def put(self, key, val):
        """Add node.

        Args:
            key (any): key of node.
            val (any): value at node.

        """
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, val, current_node):
        if key == current_node.key:
            current_node.replace_node_data(key, val, current_node.has_left_child(),
                                           current_node.has_right_child())
        elif key < current_node.key:
            if current_node.has_left_child():
                self._put(key, val, current_node.left_child)
            else:
                current_node.left_child = TreeNode(key, val, parent=current_node)
        else:
            if current_node.has_right_child():
                self._put(key, val, current_node.right_child)
            else:
                current_node.right_child = TreeNode(key, val, parent=current_node)

    def get(self, key):
        """Get node.

        Args:
            key (any): key of node.

        Returns:
            (any): value at node.

        """
        if self.root:
            res = self._get(key, self.root)
            if res:
                   return res.payload
            else:
                   return None
        else:
            return None

    def _get(self, key, current_node):
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node
        elif key < current_node.key:
            return self._get(key, current_node.left_child)
        else:
            return self._get(key, current_node.right_child)

    def delete(self, key):
        """Delete node.

        Args:
            key (any): key of node.

        """
        if self.size > 1:
            node_to_remove = self._get(key, self.root)
            if node_to_remove:
                self.remove(node_to_remove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key {} not in tree'.format(key))
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key {} not in tree'.format(key))

    def remove(self, current_node):
        """Remove node from tree.

        Args:
            current_node (TreeNode): node to remove.

        """
        if current_node.is_leaf():
            if current_node == current_node.parent.left_child:
                current_node.parent.left_child = None
            else:
                current_node.parent.right_child = None
        elif current_node.has_both_children():
            succ = current_node.find_successor()
            succ.splice_out()
            current_node.key = succ.key
            current_node.payload = succ.payload
        else:
            if current_node.has_left_child():
                if current_node.is_left_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.left_child
                elif current_node.is_right_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.left_child
                else:
                    current_node.replace_node_data(current_node.left_child.key,
                                                   current_node.left_child.payload,
                                                   current_node.left_child.left_child,
                                                   current_node.left_child.right_child)
            else:
                if current_node.is_left_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.right_child
                elif current_node.is_right_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.right_child
                else:
                    current_node.replace_node_data(current_node.right_child.key,
                                                   current_node.right_child.payload,
                                                   current_node.right_child.left_child,
                                                   current_node.right_child.right_child)


class TreeNode:
    """Node of binary search tree.

    Attributes:
        key (any): key of node.
        payload (any): value at node.
        left_child (TreeNode): possible left child node.
        right_child (TreeNode): possible right child node.
        parent (TreeNode): parent node.

    """

    def __init__(self, key, val, left=None, right=None, parent=None):
        """Constructor.

        Args:
            key (any): key of node.
            val (any): value at node.
            left (TreeNode): possible left child node.
            right (TreeNode): possible right child node.
            parent (TreeNode): parent node.

        """
        self.key = key
        self.payload = val
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def has_left_child(self):
        """Get left child of node.

        Returns:
            (TreeNode): possible left child node.

        """
        return self.left_child

    def has_right_child(self):
        """Get right child of node.

        Returns:
            (TreeNode): possible right child node.

        """
        return self.right_child

    def is_left_child(self):
        """Check if node is left child of parent node.

        Returns:
            (bool): if node is left child of a parent node.

        """
        return self.parent and self.parent.left_child == self

    def is_right_child(self):
        """Check if node is right child of parent node.

        Returns:
            (bool): if node is right child of a parent node.

        """
        return self.parent and self.parent.right_child == self

    def is_root(self):
        """Check if node is root node of tree.

        Returns:
            (bool): if node is root node of tree.

        """
        return not self.parent

    def is_leaf(self):
        """Check if node is leaf node (does not have child nodes).

        Returns:
            (bool): if node is leaf node.

        """
        return not (self.right_child or self.left_child)

    def has_any_children(self):
        """Check if node has any child nodes.

        Returns:
            (bool): if node has any child nodes.

        """
        return self.right_child or self.left_child

    def has_both_children(self):
        """Check if node has both right and left child nodes.

        Returns:
            (bool): if node has both right and left child nodes.

        """
        return self.right_child and self.left_child

    def __iter__(self):
        """Iterator.

        Yields:
            keys in tree.

        """
        if self:
            if self.has_left_child():
                for elem in self.left_child:
                    yield elem
            yield self.key
            if self.has_right_child():
                for elem in self.right_child:
                    yield elem

    def replace_node_data(self, key, value, lc, rc):
        """Replace node with a new one.

        Args:
            key (any): key of node.
            value (any): value at node.
            lc (TreeNode): possible left child node.
            rc (TreeNode): possible right child node.

        """
        self.key = key
        self.payload = value
        self.left_child = lc
        self.right_child = rc
        if self.has_left_child():
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self

    def find_successor(self):
        """Find successor node.

        Returns:
            (TreeNode): successor node.

        """
        succ = None
        if self.has_right_child():
            succ = self.right_child.find_min()
        else:
            if self.parent:
                if self.is_left_child():
                    succ = self.parent
                else:
                    self.parent.right_child = None
                    succ = self.parent.find_successor()
                    self.parent.right_child = self
        return succ

    def find_min(self):
        """Find the node with minimum key in a subtree.

        Returns:
            (TreeNode): node with min key.

        """
        current = self
        while current.has_left_child():
            current = current.left_child
        return current

    def splice_out(self):
        """Use to grab successor node while deletion."""
        if self.is_leaf():
            if self.is_left_child():
                self.parent.left_child = None
            else:
                self.parent.right_child = None
        elif self.has_any_children():
            if self.has_left_child():
                if self.is_left_child():
                    self.parent.left_child = self.left_child
                else:
                    self.parent.right_child = self.left_child
                self.left_child.parent = self.parent
            else:
                if self.is_left_child():
                    self.parent.left_child = self.right_child
                else:
                    self.parent.right_child = self.right_child
                self.right_child.parent = self.parent

def test_tree():
    tree = BinarySearchTree()
    tree[3] = 3
    tree[5] = 5
    tree[6] = 6

    #print(tree[5])
    #tree[5] = 'd'
    #print(tree[5])

    #print(len(tree))
    #del tree[5]
    #print(tree[6])
    #print(len(tree))

    for item in tree:
        print(item)
    
    print("tree : ",tree[7])
    print("tree : ",tree[3])

if __name__ == "__main__":
    test_tree()
