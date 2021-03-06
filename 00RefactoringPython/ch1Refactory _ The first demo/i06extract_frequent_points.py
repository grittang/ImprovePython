# 实例是一个影片出租店用的程序：
# 计算每一个顾客的消费金额并且打印详单,操作者告诉程序：顾客租了那些影片，租期，程序算出费用
# 影片分3类：普通片、儿童片、新片
# 除计算费用，还要为顾客积分，积分根据租片种类是否为新片有不同

# 本次新加需求：
# 1.html显示
# 2. 适应会改变的计价规则

from abc import ABC, abstractmethod

# 进入state模式花了力气，收获是：如果要修改价格有关行为
# 或者添加新的定价标准，或者加入其他取决于价格的行为，程序修改容易很多
class Price(ABC):
    @abstractmethod
    def get_price_code(self):
        pass

    @abstractmethod
    def get_charge(self, days_rented):
        pass

    def get_frequent_renter_points(self, days_rented):
        return 1

class ChildrenPrice(Price):
    def get_price_code(self):
        return Movie.childrens

    def get_charge(self, days_rented):
        result = 1.5
        if days_rented > 3:
            result += (days_rented - 3) * 1.5
        return result

    def get_frequent_renter_points(self, days_rented):
        return 1

class NewReleasePrice(Price):
    def get_price_code(self):
        return Movie.new_release

    def get_charge(self, days_rented):
        return days_rented  * 3

    def get_frequent_renter_points(self, days_rented):
        return 2 if (days_rented > 1) else 1

class RegularPrice(Price):
    def get_price_code(self):
        return Movie.regular

    def get_charge(self, days_rented):
        result = 2
        if days_rented > 2:
            result += (days_rented - 2) * 1.5
        return result

    def get_frequent_renter_points(self, days_rented):
        return 1

class Movie:
    regular = 0
    new_release = 1
    childrens = 2

    def __init__(self, title, pricecode):
        self.title = title
        # self.pricecode = pricecode
        self.price = self.set_pricecode(pricecode)
        self.pricecode = self.price.get_price_code()

    def set_pricecode(self, arg):
        if arg == Movie.regular:
            return RegularPrice()
        elif arg == Movie.childrens:
            return  ChildrenPrice()
        elif arg == Movie.new_release:
            return NewReleasePrice()
        else:
            raise Exception("Wrong!")

    def get_charge(self, days_rented):
        return self.price.get_charge(days_rented)

    def get_frequent_renter_points(self, days_rented):
        return self.price.get_frequent_renter_points(days_rented)


class Rental:
    def __init__(self, movie, days_rented):
        self.movie = movie
        self.days_rented = days_rented

    def get_charge(self):
        return self.movie.get_charge(self.days_rented)

    def get_frequent_renter_points(self):
        return self.movie.get_frequent_renter_points(self.days_rented)

class Customer:
    def __init__(self, name):
        self.name = name
        self.rentals = []

    def add_rental(self, rental):
        self.rentals.append(rental)

    def statement(self):

        def get_total_charge():
            total_amount = 0
            for rental in self.rentals:
                total_amount += rental.get_charge()
            return total_amount

        def get_total_frequent_renter_points():
            frequent_renter_points = 0
            for rental in self.rentals:
                frequent_renter_points += rental.get_frequent_renter_points()
            return frequent_renter_points


        result = "Rental record for " + self.name + "\n"
        for rental in self.rentals:

            result += "\t" + rental.movie.title + "\t" +\
                        str(rental.get_charge()) + "\n"
        result += "Amount owed is " + str(get_total_charge()) + "\n"
        result += "You earned " + str(get_total_frequent_renter_points()) + \
                    " frequent renter points"
        return result


def main():
    c0 = Customer("Bill")
    movie0 = Movie("Die hard", 0)
    movie1 = Movie("Fifty Shades Freed", 1)
    movie2 = Movie("Peter Rabbit", 2)
    rental0 = Rental(movie0, 3)
    rental1 = Rental(movie1, 4)
    rental2 = Rental(movie2, 5)
    c0.add_rental(rental0)
    c0.add_rental(rental1)
    c0.add_rental(rental2)

    # 测试代码：
    assert ('Amount owed is 20.0' in c0.statement() )
    assert ('You earned 4 frequent renter points' in c0.statement() )

    print(c0.statement())

if __name__ == "__main__":
    main()
