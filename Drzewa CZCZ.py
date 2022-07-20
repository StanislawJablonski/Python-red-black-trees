import sys
import random


# Tworzenie struktury komórki w drzewie
class Node():
    def __init__(self, data):
        self.data = data
        self.parent = None    # None - służy do zdefiniowania wartości NULL , albo braku wartości, Tylko None = None
        self.left = None
        self.right = None
        self.color = 1        # color 1 = red        color 0 = black
                              # Wstawiana komórka zawsze jest czerwona, więc domyślnie kolor jest czerwony


class RedBlackTree():
    def __init__(self):
        self.ZERO = Node
        self.ZERO.color = 0        # Korzeń zawsze czarny
        self.ZERO.left = None
        self.ZERO.right = None
        self.root = self.ZERO


        # Wstawianie
    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.ZERO
        node.right = self.ZERO
        node.color = 1

        y = None
        x = self.root

        while x != self.ZERO:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

        # Naprawia drzewo po wstawieniu

    def fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rotate_right(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rotate_left(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.rotate_left(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.rotate_right(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0



    # Wypisywanie
    def print_exec(self, node, x, last):
        if node != self.ZERO:
            sys.stdout.write(x)
            if last:
                sys.stdout.write("R----")
                x += "     "
            else:
                sys.stdout.write("L----")
                x += "|    "

            s_color = "Red" if node.color == 1 else "Black"
            print(str(node.data) + "(" + s_color + ")")
            self.print_exec(node.left, x, False)
            self.print_exec(node.right, x, True)

    # Zwraca minimalną wartość komórki
    def minimum(self, node):
        while node.left != self.ZERO:
            node = node.left
        return node

    # Zwraca maksymalną wartość komórki
    def maximum(self, node):
        while node.right != self.ZERO:
            node = node.right
        return node

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.ZERO:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.ZERO:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y


    def get_root(self):
        return self.root

    def print_tree(self):
        self.print_exec(self.root, "", True)


    def change(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Usowanie komórki
    def delete_exec(self, node, key):
        z = self.ZERO
        while node != self.ZERO:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.ZERO:
            print("The key is not in the tree!\n")
            return

        y = z
        y_original_color = y.color
        if z.left == self.ZERO:
            x = z.right
            self.change(z, z.right)
        elif (z.right == self.ZERO):
            x = z.left
            self.change(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.change(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.change(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.delete_fix(x)

    # Naprawa po usowaniu
    def delete_fix(self, x):
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.rotate_left(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.rotate_right(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.rotate_right(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.rotate_left(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = 0


    def delete_node(self, data):
        self.delete_exec(self.root, data)


    def find_depth(self):

        def find_depth_exec(node):
            left_height = right_height = 0
            if node.left:
                left_height = find_depth_exec(node.left) + 1
            if node.right:
                right_height = find_depth_exec(node.right) + 1
            return max(left_height, right_height)

        return find_depth_exec(self.root)


    def find_min_depth(self):

        def find_min_depth_exec(node):
            left_height = right_height = 0
            if node.left:
                left_height = find_min_depth_exec(node.left) + 1
            if node.right:
                right_height = find_min_depth_exec(node.right) + 1
            return min(left_height, right_height)

        return find_min_depth_exec(self.root)


    def count_red(self):
        def count_red_exec(node):
            if node == None:
                return 0

            if node.color == 1:
                return 1 + count_red_exec(node.left) + count_red_exec(node.right)
            else:
                return count_red_exec(node.left) + count_red_exec(node.right)

        return count_red_exec(self.root)



if __name__ == "__main__":
    bst = RedBlackTree()

    bst.insert(38)
    bst.insert(31)
    bst.insert(22)
    bst.insert(8)
    bst.insert(20)
    bst.insert(5)
    bst.insert(10)
    bst.insert(9)
    bst.insert(21)
    bst.insert(27)
    bst.insert(29)
    bst.insert(25)
    bst.insert(28)

    bst.print_tree()

    bst.delete_node(28)

    bst.print_tree()

    height = bst.find_depth()
    min_height = bst.find_min_depth()
    print("MAX depth = " + str(height) + "   MIN depth = " + str(min_height) + ".")

    count_red = bst.count_red()
    print("Number of red nodes = " + str(count_red))

    """
    for x in range(0,1001):
        bst.insert(random.randrange(0,10000,1))

    bst.print_tree()
    height = bst.find_depth()
    min_height = bst.find_min_depth()
    print("MAX depth = " + str(height) + "   MIN depth = " + str(min_height) + ".")
    count_red = bst.count_red()
    print("Number of red nodes = " + str(count_red))
    """







