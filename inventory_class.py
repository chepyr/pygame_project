class Inventory:
    def __init__(self):
        self.inventory_content = list()

    def print_content(self):
        print('Содержимое инвентаря: ', end='')
        for item in self.inventory_content:
            print(item.name, end=' ')
        print()

    def add_item(self, new_item):
        self.inventory_content.append(new_item)

    def has(self, find_item):
        for item in self.inventory_content:
            if item.name == find_item:
                return True
        return False

