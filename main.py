import sys
import time


class Dot:
    """Класс виксирующий, точки корбаля по x и y"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Errors:  # не знаю зачем он так нужен, как по мне, то проще настолько простые условия прописать внутри функции
    """Класс ошибок"""

    @staticmethod
    def out(dot):
        if 6 >= dot.x >= 1 and 6 >= dot.y >= 1:
            return False
        else:
            return True


class Ship:
    """" Класс корабля, его длины, направления (горизонталь\вертикаль), координаты носа корбаля"""

    def __init__(self, length, direction, nose):

        self.length = length
        self.direction = direction
        self.live = int(length)
        self.nose = nose

    def dots(self):
        """Возвращает координаты носа корбаля"""
        dots = []
        if self.direction == "Vertical":
            for i in range(self.length):
                dots.append(Dot(self.nose.x + i, self.nose.y))
        elif self.direction == "Horizontal":
            for i in range(self.length):
                dots.append(Dot(self.nose.x, self.nose.y + i))
        else:
            raise ValueError("Неправильные координаты носа")
        return dots


def my_game_board():
    """Игровое поле"""
    Array_Matrix = [["|О|" for _ in range(7)] for _ in range(7)]

    for num in range(1, 7):
        Array_Matrix[num][0] = str(num)

    for num_1 in range(7):
        if num_1 == 0:
            Array_Matrix[0][0] = str(" ")
        else:
            Array_Matrix[0][num_1] = str(f" {num_1} ")
    return Array_Matrix


def enemy_board():
    """Вражеское поле"""

    Array_Matrix_enemy = [["|О|" for _ in range(7)] for _ in range(7)]

    for num in range(1, 7):
        Array_Matrix_enemy[num][0] = str(num)

    for num_1 in range(7):
        if num_1 == 0:
            Array_Matrix_enemy[0][0] = str(" ")
        else:
            Array_Matrix_enemy[0][num_1] = str(f" {num_1} ")
    return Array_Matrix_enemy


class Board:
    """Класс игровой доски"""

    def __init__(self, hidden=False, game_board=None):
        self.game_board = game_board
        self.ships = []
        self.hidden = hidden
        self.count_live_ships = 0
        self.ghost_board = [row.copy() for row in self.game_board]

    def check_add_ship(self, ship):
        """Проверка постановки корабля"""
        for dot in ship.dots():
            if not (6 >= dot.x >= 1 and 6 >= dot.y >= 1):
                return False
            if self.game_board[dot.x][dot.y] != "|О|":
                if (ship.length - dot.y) < 0 or (ship.length - dot.x) < 0:
                    return True
                else:
                    for i in range(dot.x - 1, dot.x + ship.length + 1):
                        for j in range(dot.y - 1, dot.y + 2):
                            if (1 <= i <= 6 and 1 <= j <= 6 and
                                    self.game_board[i][j] != "|О|"):
                                return False
                        return True
        return True

    def check_distance(self, ship):
        """Проверка дистанции корабля"""
        for dot in ship.dots():
            if dot.x < 1 or dot.x > 6 or dot.y < 1 or dot.y > 6:
                return False
            for i in range(ship.length):
                if ship.direction == "Horizontal":
                    if i == 0:
                        if dot.y - ship.length // 3 >= 1 and self.game_board[dot.x][dot.y - ship.length // 3] == "|■|":
                            return False
                    elif i == ship.length - 1:
                        if dot.y + ship.length // 3 + 1 <= 6 and self.game_board[dot.x][
                            dot.y + ship.length // 3 + 1] == "|■|":
                            return False
                    else:
                        if dot.y - ship.length // 3 >= 1 and self.game_board[dot.x][
                            dot.y - ship.length // 3] == "|■|" or dot.y + i <= 6 and self.game_board[dot.x][
                            dot.y + i] == "|■|" or dot.x - ship.length // 3 >= 1 and \
                                self.game_board[dot.x - ship.length // 3][dot.y] == "|■|" or dot.x + i <= 6 and \
                                self.game_board[dot.x + i][dot.y] == "|■|":
                            return False
                elif ship.direction == "Vertical":
                    if i == 0:
                        if dot.x - ship.length // 3 >= 1 and self.game_board[dot.x - ship.length // 3][dot.y] == "|■|":
                            return False
                    elif i == ship.length - 1:
                        if dot.x + ship.length // 3 + 1 <= 6 and self.game_board[dot.x + ship.length // 3 + 1][
                            dot.y] == "|■|":
                            return False
                    else:
                        if dot.x - ship.length // 3 >= 1 and self.game_board[dot.x - ship.length // 3][
                            dot.y] == "|■|" or dot.x + i <= 6 and self.game_board[dot.x + i][
                            dot.y] == "|■|" or dot.y - ship.length // 3 >= 1 and self.game_board[dot.x][
                            dot.y - ship.length // 3] == "|■|" or dot.y + i <= 6 and self.game_board[dot.x][
                            dot.y + i] == "|■|":
                            return False
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if 7 > dot.x + i + j >= 1 and 7 > dot.y + i + k >= 1:
                            if self.game_board[dot.x + i + j][dot.y + i + k] != "|О|" and \
                                    self.game_board[dot.x + i + j][
                                        dot.y + i + k] != ".":
                                return False
        return True

    def check_placement(self, ship):  # Я без понятия, что тут наворотил, но оно как-то работает:)
        """Проверка постановки корабля финальная"""

        if not self.check_distance(ship):
            return False
        for dot in ship.dots():
            if dot.x < 1 or dot.x > 6 or dot.y < 1 or dot.y > 6:
                return False
            for existing_ship in self.ships:
                if existing_ship != ship:
                    for dot2 in existing_ship.dots():
                        if dot.x == dot2.x and abs(dot.y - dot2.y) <= 1 or dot.y == dot2.y and abs(dot.x - dot2.x) <= 1:
                            if ship.length + existing_ship.length <= 3:
                                return False
        return True

    def show_board(self):
        """"Показать игровое поле"""
        for row in self.game_board:
            print(" ".join(row))

    def hidden_board(self):
        """Скрыть корабли"""
        if not self.hidden:
            self.show_board()

    def add_ship(self, ship):
        """Добавление корабля"""
        while True:
            if not self.check_add_ship(ship):
                return False
            else:
                if not self.check_placement(ship):
                    return False
                else:
                    for dot in ship.dots():
                        self.game_board[dot.x][dot.y] = "|■|"

                    self.ships.append(ship)
                    self.hidden_board()
                    self.count_live_ships += 1
                    return True

    def contour(self, ship):
        """Отрисовка уничтоженого корабля по контуру"""
        for dot in ship.dots():
            for i in range(-1, 2):

                for j in range(-1, 2):
                    if 7 > dot.x + i >= 1 and 7 > dot.y + j >= 1:
                        self.game_board[dot.x + i][dot.y + j] = "|X|"

    def shot(self, dot):
        """Выстрел ппо короблю, логика промаха и попаадния"""
        if Errors.out(dot):
            raise ValueError("Выстрел за границей баталии!")

        if self.game_board[dot.x][dot.y] in ["|X|", "|T|"]:
            print("Вы уже сюда стреляли!")
            time.sleep(1)
            return False

        if self.game_board[dot.x][dot.y] == "|■|":
            self.game_board[dot.x][dot.y] = "|X|"
            if self.hidden_board():
                self.show_board()
            time.sleep(1)
            print("Есть пробитие!")
            for ship in self.ships:
                if dot in ship.dots():
                    ship.live -= 1
                    if ship.live == 0:
                        self.contour(ship)
                        self.count_live_ships -= 1
                        time.sleep(1)
                        print("Корабль уничтожен!")
            return True
        elif self.game_board[dot.x][dot.y] == "|О|":
            self.game_board[dot.x][dot.y] = "|T|"
            if self.hidden_board():
                self.show_board()
            time.sleep(1)
            print("Промах!")
            return False

    def shot_ghost(self, dot):
        if self.game_board[dot.x][dot.y] == "|■|":
            self.game_board[dot.x][dot.y] = "|X|"
            self.ghost_board[dot.x][dot.y] = "|T|"
            if self.hidden:
                self.show_board()
            return True
        elif self.game_board[dot.x][dot.y] == "|О|":
            self.ghost_board[dot.x][dot.y] = "|T|"


class Player:
    """Класс игрока в игру (и AI, и пользователь)"""

    def __init__(self):
        self.game_board = my_game_board()
        self.enemy_board = enemy_board

    def ask(self):
        """ метод, который «спрашивает» игрока, в какую клетку он делает выстрел"""
        y = 0
        x = 0
        return Dot(x, y)

    # def move(self):
    #     """Метод, который делает ход в игре."""
    #     print("Выстрел производится")
    #     while True:
    #         if Board().shot(self.ask()):
    #             continue
    #         else:
    #             break


class User(Player):
    """Игрок-пользователь"""

    def ask(self):
        """Метод, который «спрашивает» игрока, в какую клетку он делает выстрел"""
        x = int(input("Введите координату x: "))
        y = int(input("Введите координату y: "))
        return Dot(x, y)

    # def move(self):
    #     print("Выстрел производится")
    #     while True:
    #         if Board(hidden=False, game_board=self.enemy_board).shot(self.ask()):
    #             continue
    #         else:
    #             break


class Ai(Player):
    """Игрок-AI"""

    def ask(self):
        """Метод, который «спрашивает» игрока, в какую клетку он делает выстрел"""
        import random
        y = random.randint(1, 6)
        x = random.randint(1, 6)
        return Dot(x, y)

    def move(self):
        print("Выстрел противника производится")
        while True:
            if Board(hidden=False, game_board=self.game_board).shot(self.ask()):
                continue
            else:
                break


class Game:
    """Класс игры, здесь происходит самое вкусное"""

    def __init__(self):
        self.user = User()
        self.my_game_board = User().game_board
        self.Ai = Ai()
        self.enemy_board = self.random_board()

    def random_board(self):
        """Созадние случайной доски противника"""
        attempt = 0  # счетчик попыток успешный корабелй
        count = 0  # счетчик попыток всех попыток
        enemy_board_1 = enemy_board()
        board_enm = Board(hidden=True, game_board=enemy_board_1)
        for num in (3, 2, 2, 1, 1, 1, 1):
            while True:
                if count > 1000:
                    return self.random_board()
                if attempt > 7:
                    break
                import random
                side = random.randint(1, 2)
                if side == 1:
                    ship_num = board_enm.add_ship(Ship(num, "Vertical", self.Ai.ask()))
                    if not ship_num:
                        count += 1
                        continue
                    else:
                        count += 1
                        attempt += 1
                        break
                elif side == 2:
                    ship_num = board_enm.add_ship(Ship(num, "Horizontal", self.Ai.ask()))
                    if not ship_num:
                        count += 1
                        continue
                    else:
                        count += 1
                        attempt += 1
                        break

                if attempt > 7:
                    break

    @staticmethod
    def cls():
        """Очистка экрана"""
        print("\n" * 22)

    @staticmethod
    def loading_screen():
        """Отображение милой загрузки игры"""
        for i in range(12):
            time.sleep(0.3)
            if i % 2 != 0:
                print("✿", end="")
            else:
                print("♡", end="")
        return print("Отлично!")

    def greet(self):
        """Вступление"""
        print("""

        █░█░█ █▀▀ █░░ █▀▀ █▀█ █▀▄▀█ █▀▀   ▀█▀ █▀█   ▀█▀ █░█ █▀▀  
        ▀▄▀▄▀ ██▄ █▄▄ █▄▄ █▄█ █░▀░█ ██▄   ░█░ █▄█   ░█░ █▀█ ██▄  

                    █▄▄ ▄▀█ ▀█▀ ▀█▀ █░░ █▀▀ █▀ █░█ █ █▀█
                    █▄█ █▀█ ░█░ ░█░ █▄▄ ██▄ ▄█ █▀█ █ █▀▀
        """)
        time.sleep(1.8)
        self.cls()
        print("Сейчас вы погрузитесь в увлекательную игру, которую именуют в простонародье - МОРСКОЙ БОЙ!!! \n")
        time.sleep(2)
        print("Но для начала нуно ознакомиться с правилами игры!")

        rules = """Правила игры:

            1.Каждый игрок имеет два  квадрата размером 6×6 клеток.

            2.Вертикаль нумеруется цифрами сверху вниз. По горизонтали под каждой клеткой записываются также цифры от «1» до «6».

            3.В одном квадрате игрок скрытно от противника расставляет свои корабли. Другое поле — пустое, здесь игрок будет отмечать подбитые корабли противника.

            4.Игрок, получивший право первым начать игру, производит «выстрел», назвав один из координат, например, «1 3».

            5.Если эта клетка занята частью корабля или всем кораблем, то противник соответственно говорит «ранен» или «убит». Участник получает право еще на один ход.

            6.Если в названной им клетке нет корабля, ход переходит сопернику, а в клетке ставится буква "T".

            7.Игра ведется до тех пор, пока у одного из участников не будут потоплены все корабли."""

        while True:
            answer = input("Нажмите Enter для продолжения: ")
            if answer == "":
                print("OK")
                time.sleep(1)
                print(rules)
                answer = input("Если вы уже ознакомились с правилами, то Enter для продолжения: ")
                if answer == "":
                    self.cls()
                    break
            else:
                print("Это не Enter!")
                Exit = input(
                    "Нажмите 'E' если хотите выйти из игры: ")  # хотел добавить хоткей на esc, но что-то не получилось, мб оно в тинкере нормально работает
                if Exit != "E":
                    self.cls()
                    continue
                else:
                    print("До новых встреч!")
                    sys.exit(0)
        print("Время начинать игру, подготовка игрока и соперника(AI)")
        self.loading_screen()
        time.sleep(1)
        self.cls()

    # def places_player_ship(self):
    #     """Ставим корабли свои"""
    #     print("Нужно расставить НАШИ корабли...")
    #     time.sleep(0.5)
    #     count = 0  # счетчик удачных кораблей
    #     board_my = Board(hidden=False, game_board=self.my_game_board)
    #     for num in (3, 2, 2, 1, 1, 1, 1):
    #         if count >= 7:
    #             break
    #         while True:
    #             print(f"Сейчас вы ставите корабль длинной: {num}, осталось кораблей:{7 - count} .")
    #             if count >= 3:
    #                 my_ship = board_my.add_ship(Ship(num, "Vertical", self.user.ask()))
    #                 if not my_ship:
    #                     print("Неизвестное направление!")
    #                     continue
    #                 else:
    #                     count += 1
    #                     break
    #
    #             direction = input("Выберите как будете ставить корабль - vert(вертикаль) или horz(горизонталь):")
    #             board_my.show_board()
    #
    #             if direction == "horz":
    #                 my_ship = board_my.add_ship(Ship(num, "Horizontal", self.user.ask()))
    #                 if not my_ship:
    #                     continue
    #                 else:
    #                     count += 1
    #                     break
    #             elif direction == "vert":
    #                 my_ship = board_my.add_ship(Ship(num, "Vertical", self.user.ask()))
    #                 if not my_ship:
    #                     continue
    #                 else:
    #                     count += 1
    #                     break
    #             else:
    #                 print("Неизвестная направлене!")
    #                 continue
    #
    #     print("Все ваши корабли установлены!")
    #     print(f"Количество кораблей:{board_my.count_live_ships}")

    @staticmethod
    def first_move():
        """Рандом перввого хода"""
        import random
        move_first = random.randint(1, 2)
        if move_first == 2:
            return True
        else:
            return False

    def win_and_lose(self, game_board, enemy):
        if enemy.count_live_ships < 1:
            print("Вы выиграли!")
            return True
        elif game_board.count_live_ships < 1:
            print("Вы проиграли!")
            return True

    def loop(self):
        """Игровой процесс"""
        """Ставим корабли свои"""
        print("Нужно расставить НАШИ корабли...")
        time.sleep(0.3)
        count = 0  # счетчик удачных кораблей
        board_my = Board(hidden=False, game_board=self.my_game_board)
        for num in (3, 2, 2, 1, 1, 1, 1):
            if count >= 7:
                break
            while True:
                print(f"Сейчас вы ставите корабль длинной: {num}, осталось кораблей:{7 - count} .")
                if count >= 3:
                    my_ship = board_my.add_ship(Ship(num, "Vertical", self.user.ask()))
                    if not my_ship:
                        print("Неизвестное направление!")
                        continue
                    else:
                        count += 1
                        break

                direction = input("Выберите как будете ставить корабль - vert(вертикаль) или horz(горизонталь):")
                board_my.show_board()

                if direction == "horz":
                    my_ship = board_my.add_ship(Ship(num, "Horizontal", self.user.ask()))
                    if not my_ship:
                        continue
                    else:
                        count += 1
                        break
                elif direction == "vert":
                    my_ship = board_my.add_ship(Ship(num, "Vertical", self.user.ask()))
                    if not my_ship:
                        continue
                    else:
                        count += 1
                        break
                else:
                    print("Неизвестная направлене!")
                    continue

        print("Все ваши корабли установлены!")
        print(f"Количество кораблей:{board_my.count_live_ships}")

        attempt = 0  # счетчик попыток успешный корабелй
        count = 0  # счетчик попыток всех попыток
        enemy_board_1 = enemy_board()
        board_enm = Board(hidden=True, game_board=enemy_board_1)
        for num in (3, 2, 2, 1, 1, 1, 1):
            while True:
                if count > 1000:
                    return self.random_board()
                if attempt > 7:
                    break
                import random
                side = random.randint(1, 2)
                if side == 1:
                    ship_num = board_enm.add_ship(Ship(num, "Vertical", self.Ai.ask()))
                    if not ship_num:
                        count += 1
                        continue
                    else:
                        count += 1
                        attempt += 1
                        break
                elif side == 2:
                    ship_num = board_enm.add_ship(Ship(num, "Horizontal", self.Ai.ask()))
                    if not ship_num:
                        count += 1
                        continue
                    else:
                        count += 1
                        attempt += 1
                        break

                if attempt > 7:
                    break
        self.loading_screen()
        print("Корабли противника установлены!")

        move = self.first_move()
        move_1 = 0
        while True:
            if move:
                if self.win_and_lose(board_my, board_enm):
                    break
                print("Ход делаете вы:")
                if not board_enm.shot(self.user.ask()):
                    move_1 += 1
                    move = not move

            else:
                if self.win_and_lose(board_my, board_enm):
                    break
                print("Ход делает противник!")
                if not board_my.shot(self.Ai.ask()):
                    move_1 += 1
                    move = not move

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()


