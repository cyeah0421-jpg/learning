from turtledemo.penrose import start


class Goods:
    """
    商品类 :用于存储单个商品的名称，价格和数量
    """
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"商品名称：{self.name}，价格：{self.price}，数量：{self.quantity}"

class ShoppingCart:
    """
    购物车类 :用于存储用户购买的商品
    """
    def __init__(self):
        self.cart_items = []

    def add_item(self):
        """
        添加商品到购物车
        """
        print("-------添加商品--------")
        name = input("请输入商品名称：")
        # 简单的输入校验 防止价格为非法数字
        try:
            price = float(input("请输入商品价格："))
        except ValueError:
            print("价格输入错误，请重新输入")
            return
        try:
            quantity = int(input("请输入商品数量："))
        except ValueError:
            print("数量输入错误，请重新输入")
            return
        item = Goods(name, price, quantity)

        self.cart_items.append(item)
        print(f"商品{name}添加成功")

    def modify_item(self):
        """
        修改购物车中的商品信息
        """
        print("-------修改商品信息--------")
        name = input("请输入要修改的商品名称：")
        for item in self.cart_items:
            if item.name == name:
                print(f"当前商品信息：{item}")
                print("请选择要修改的属性：")
                print("1. 修改商品名称")
                print("2. 修改商品价格")
                print("3. 修改商品数量")
                choice = input("请输入您的选择：")
                if choice == "1":
                    new_name = input("请输入新的商品名称：")
                    item.name = new_name
                    print(f"商品名称修改成功，新的商品名称为：{new_name}")
                elif choice == "2":
                    try:
                        new_price = float(input("请输入新的商品价格："))
                        item.price = new_price
                        print(f"商品价格修改成功，新的商品价格为：{new_price}")
                        print(f"商品{item.name}修改成功")
                        print(item)
                    except ValueError:
                        print("价格输入错误，请重新输入")
                        return
        print("商品修改失败")

    def remove_item(self):
        """
        从购物车中删除商品
        """
        print("-------删除商品--------")
        name = input("请输入要删除的商品名称：")
        for item in self.cart_items:
            if item.name == name:
                self.cart_items.remove(item)
                print(f"商品{name}删除成功")
                return
        print("商品删除失败")

    def query_item(self):
        """
        查询购物车中的商品信息
        """
        print("-------查询商品信息--------")
        if len(self.cart_items) == 0:
            print("购物车为空")
        else:
            for index,item in enumerate(self.cart_items,start = 1):
                print(f"商品{index}信息：{item}")

    def run(self):
        """
        运行购物车程序
        """
        while True:
            print("-------购物车管理系统--------")
            print("1. 添加商品")
            print("2. 修改商品信息")
            print("3. 删除商品")
            print("4. 查询商品信息")
            print("5. 退出系统")
            choice = input("请输入您的选择：")
            if choice == "1":
                self.add_item()
            elif choice == "2":
                self.modify_item()
            elif choice == "3":
                self.remove_item()
            elif choice == "4":
                self.query_item()
            elif choice == "5":
                print("退出系统")
                break
            else:
                print("无效的选择，请重新输入")

if __name__ == "__main__":
    cart = ShoppingCart()
    cart.run()