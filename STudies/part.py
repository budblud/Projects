class IncorrectValueError(ValueError):
    pass

class Stores:

    def __init__(self, name: str, items: list, prices: list):

        self.name = name
        self.items = items
        self.prices = prices

    def all_prices_for_each_item(self):
        new_price_list = []
        if len(self.items) == len(self.prices):
            for i in range(len(self.prices)):
                new_price_list.append((self.items[i], self.prices[i]))
            return new_price_list
        else:
            raise IncorrectValueError(
                f"The quantity of items,{len(self.items)}, do not correspond to the quantity of prices,{len(self.prices)}."
            )

store = Stores(name= 'My Wonderful Store', items= ["Chair", "Table", "Socks", "Bottle"], prices= [1, 15.99, 21.76, 3, 1.3])

print(store.all_prices_for_each_item())