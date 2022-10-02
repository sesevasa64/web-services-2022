from typing import List
from app.contracts import User, UserRegistration, Product, ProductRegistration

class UserAlreadyExistError(Exception):
    pass

class UserNotExistError(Exception):
    pass

class ProductAlreadyExistError(Exception):
    pass

class ProductNotExistError(Exception):
    pass

class Database:
    uuid2user = {}
    login2user = {}
    puid2product = {}
    name2product = {}
    user_uid_counter = 0
    prod_uid_counter = 0
    def __init__(self):
        # Пришлось добавить self переменные, т.к vscode почему-то не видит переменные класса
        self.uuid2user = Database.uuid2user
        self.login2user = Database.login2user
        self.puid2product = Database.puid2product
        self.name2product = Database.name2product
        self.user_uid_counter = Database.user_uid_counter
        self.prod_uid_counter = Database.prod_uid_counter
    def add_user(self, user_reg: UserRegistration):
        if user_reg.login in self.login2user:
            raise UserAlreadyExistError
        user_uid = self.gen_user_uid()
        user = User(login=user_reg.login, password=user_reg.password, uid=user_uid)
        self.uuid2user[user_uid] = user
        self.login2user[user.login] = user
    def get_user(self, uuid: int) -> User:
        try:
            return self.uuid2user[uuid]
        except KeyError:
            raise UserNotExistError
    def add_product(self, prod_reg: ProductRegistration):
        if prod_reg.name in self.name2product:
            raise ProductAlreadyExistError
        prod_uid = self.gen_prod_uid()
        product = Product(
            name=prod_reg.name, description=prod_reg.description, 
            type=prod_reg.type, cost=prod_reg.cost, uid=prod_uid
        )
        self.puid2product[prod_uid] = product
        self.name2product[product.name] = product
    def get_products(self) -> List[Product]:
        return list(self.puid2product.values())
    def get_product(self, puid: int) -> Product:
        try:
            return self.puid2product[puid]
        except KeyError:
            raise ProductNotExistError
    def del_user(self, user_login):
        if user_login not in self.login2user:
            raise UserNotExistError
        user = self.login2user[user_login]
        del self.uuid2user[user.uid]
        del self.login2user[user.login]
        del user
    def gen_user_uid(self):
        self.user_uid_counter += 1
        return self.user_uid_counter
    def gen_prod_uid(self):
        self.prod_uid_counter += 1
        return self.prod_uid_counter
