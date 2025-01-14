class CalcUtil:
    @staticmethod
    def calc_right_down(cur, all_jewelry):
        length = 0
        row = cur.get_row()
        col = cur.get_col()
        for i, k in zip(range(row + 1, 15), range(col + 1, 6)):
            jewelry = all_jewelry[k][i]
            if jewelry.is_empty():
                break
            if jewelry.get_color() == cur.get_color():
                length += 1
            else:
                break
        return length

    @staticmethod
    def calc_right_top(cur, all_jewelry):
        length = 0
        row = cur.get_row()
        col = cur.get_col()
        for i, k in zip(range(row - 1, -1, -1), range(col + 1, 6)):
            jewelry = all_jewelry[k][i]
            if jewelry.is_empty():
                break
            if jewelry.get_color() == cur.get_color():
                length += 1
            else:
                break
        return length

    @staticmethod
    def calc_left_down(cur, all_jewelry):
        length = 0
        row = cur.get_row()
        col = cur.get_col()
        for i, k in zip(range(row + 1, 15), range(col - 1, -1, -1)):
            jewelry = all_jewelry[k][i]
            if jewelry.is_empty():
                break
            if jewelry.get_color() == cur.get_color():
                length += 1
            else:
                break
        return length

    @staticmethod
    def calc_left_top(cur, all_jewelry):
        length = 0
        row = cur.get_row()
        col = cur.get_col()
        for i, k in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            jewelry = all_jewelry[k][i]
            if jewelry.is_empty():
                break
            if jewelry.get_color() == cur.get_color():
                length += 1
            else:
                break
        return length

    @staticmethod
    def calc_down(cur, all_jewelry):
        length = 0
        index = cur.get_row()
        for i in range(index + 1, 15):
            jewelry = all_jewelry[cur.get_col()][i]
            if jewelry.is_empty():
                break
            if jewelry.get_color() == cur.get_color():
                length += 1
            else:
                break
        return length

    @staticmethod
    def calc_top(cur, all_jewelry):
        length = 0
        index = cur.get_row()
        for i in range(index - 1, -1, -1):
            jewelry = all_jewelry[cur.get_col()][i]
            if jewelry.is_empty():
                break
            if jewelry.get_color() == cur.get_color():
                length += 1
            else:
                break
        return length

    @staticmethod
    def calc_right(cur, all_jewelry):
        length = 0
        index = cur.get_col()
        for i in range(index + 1, 6):
            jewelry = all_jewelry[i][cur.get_row()]
            if jewelry.is_empty():
                break
            if jewelry.get_color() == cur.get_color():
                length += 1
            else:
                break
        return length

    @staticmethod
    def calc_left(cur, all_jewelry):
        length = 0
        index = cur.get_col()
        for i in range(index - 1, -1, -1):
            jewelry = all_jewelry[i][cur.get_row()]
            if jewelry.is_empty():
                break
            if jewelry.get_color() == cur.get_color():
                length += 1
            else:
                break
        return length