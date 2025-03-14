import json


class Item:
    def __init__(self, name: str, price: int, weight: float):
        self.name = name
        self.price = price
        self.weight = weight

    def __repr__(self):
        return f"<{self.name}: {self.price}฿ {self.weight}>"

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_weight(self):
        return self.weight


class SubBag:
    def __init__(self, weight: int):
        self.items: list[Item] = []
        self.weight = weight
        self.status = ""

    def get_abbr_items_name(self):
        return [v.get_name()[0] for v in self.items]

    def get_total_price(self):
        total_price = 0
        for v in self.items:
            total_price += v.get_price()
        return total_price

    def get_total_weight(self):
        total_weight = 0
        for v in self.items:
            total_weight += v.get_weight()
        return total_weight

    def get_items(self):
        return self.items

    def __repr__(self):
        return f"{self.status} {self.get_total_price()}฿ {self.get_total_weight()}' [{", ".join(self.get_abbr_items_name())}]"

    def add(self, item: Item, status: str):
        self.items.append(item)
        self.status = status

    def add_all(self, items: list[Item], status: str):
        self.items.extend(items)
        self.status = status


class KnapsackTable:
    def __init__(self, max_weight: int, record: list[Item], is_print_step: bool):
        self.head = self.ks_range(max_weight)
        self.record = record
        self.values = [[SubBag(h) for h in self.head] for _ in range(len(record))]
        self.is_print_step = is_print_step
        self.calculate_values()

    def ks_range(self, max_weight: int):
        return [i for i in range(max_weight + 1)]

    def calculate_values(self):
        row, col = self.get_size()
        for i in range(row):
            for j in range(col):
                p, pp, pw = self.get_prev(i, j)
                r, rp, rw = self.get_remain(i, j)
                c, cp, cw = self.get_curr(i)
                if cw <= self.head[j]:
                    if i > 0:
                        if rp + cp > pp:
                            self.values[i][j].add_all(r, '')
                            self.values[i][j].add(c, str(self.shift(i, j) + 1))
                        else:
                            self.values[i][j].add_all(p, "L")
                    else:
                        self.values[i][j].add(c, "I")
                else:
                    self.values[i][j].add_all(p, "E")
                if self.is_print_step:
                    self.show_table()

    def shift(self, i, j):
        shift_value = j - self.get_curr(i)[2]
        return max(shift_value, 0)

    def get_prev(self, i, j):
        if i == 0:
            return [], 0, 0
        prev: SubBag = self.values[i - 1][j]
        return prev.get_items(), prev.get_total_price(), prev.get_total_weight()

    def get_remain(self, i, j):
        if i == 0 or j == 0:
            return [], 0, 0
        remain: SubBag = self.values[i - 1][self.shift(i, j)]
        return remain.get_items(), remain.get_total_price(), remain.get_total_weight()

    def get_curr(self, i):
        curr: Item = self.record[i]
        return curr, curr.get_price(), curr.get_weight()

    def get_size(self):
        return len(self.record), len(self.head)

    def show_table(self):
        if self.is_print_step:
            temp = [[self.record[i]] + row for i, row in enumerate(self.values)]
            from tabulate import tabulate
            print(tabulate(temp, headers=list(map(str, self.head)), tablefmt="pipe"))
        else:
            pass

    def get_result(self):
        res = self.values[-1][-1]
        return res.get_items(), res.get_total_price(), res.get_total_weight()


def main():
    item_list = list(json.loads(input()))
    max_weight = int(input())
    items: list[Item] = []
    for v in item_list:
        items.append(Item(*v))

    knapsack_tb = KnapsackTable(max_weight, items, True)

    v, vp, vw = knapsack_tb.get_result()
    v.sort(key=lambda x: x.get_name())
    print(f"Total: {vp}")
    for item in v:
        print(f"{item.get_name()} -> {item.get_weight()} kg -> {item.get_price()} THB")


if __name__ == '__main__':
    main()
