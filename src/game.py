from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QWidget,
    QLabel,
    QFrame
)
import itertools
import random
import sys

class MainWindow(QMainWindow):
    MAP_X = 64
    MAP_Y = 32
    NUM_MINES = 10
    NUM_ZOMBIES = 15
    TICK_INTERVAL = 50 # ms
    MOVES = {
        Qt.Key_Up: (0, -1),
        Qt.Key_Down: (0, 1),
        Qt.Key_Left: (-1, 0),
        Qt.Key_Right: (1, 0)
    }
    TICKS_TO_WIN = (180 * 1000) / TICK_INTERVAL # 180 s * 1000 = 180000 ms
    ESCAPE_TIME = 5000 # ms
    ZOMBIE_RANGE = 15
    ZOMBIE_TICK_MODULO = 4
    TICKS_TO_SECOND = 1000 / TICK_INTERVAL # assume that TICK_INTERVAL <= 1000 ms

    def __init__(self):
        super().__init__()

        self.pending_move = None
        self.tick_count = 0

        self.player_x = 0
        self.player_y = 0

        self.grid_labels = [[None for _ in range(self.MAP_X)] for _ in range(self.MAP_Y)]
        self.zombies = []
        self.mines = []

        self.setWindowTitle('GrindProjectGame')
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        glayout = QGridLayout()
        main_layout.addLayout(glayout)
        for y in range(MainWindow.MAP_Y):
            for x in range(MainWindow.MAP_X):
                label = QLabel('   ', self)
                label.setStyleSheet('font-size: 16px; color: black')
                label.setAutoFillBackground(True)
                self.update_label_color(label, 'lime')
                glayout.addWidget(label, y, x)
                self.grid_labels[y][x] = label

        map_size = self.MAP_X * self.MAP_Y

        self.place_objects(
            map_size,
            self.mines,
            self.NUM_MINES,
            'blue'
        )

        self.place_objects(
            map_size - self.NUM_MINES,
            self.zombies,
            self.NUM_ZOMBIES,
            'pink',
            self.mines
        )

        player_pos = []
        self.place_objects(
            map_size - self.NUM_MINES - self.NUM_ZOMBIES,
            player_pos,
            1,
            'red',
            self.mines,
            self.zombies
        )
        self.player_x = player_pos[0][0]
        self.player_y = player_pos[0][1]
        self.grid_labels[self.player_y][self.player_x].setText('P')

        glayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setLineWidth(2)
        main_layout.addWidget(line)

        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.time_left_label = QLabel(f'Time to start: {(self.ESCAPE_TIME - self.tick_count * self.TICK_INTERVAL) / 1000}')

        hlayout.addWidget(self.time_left_label)
        main_layout.addLayout(hlayout)

        self.tick_timer = QTimer(self)
        self.tick_timer.timeout.connect(self.game_tick_a)
        self.tick_timer.start(self.TICK_INTERVAL)

    def place_objects(
        self,
        free_coords_count,
        obj_list,
        count,
        color,
        *args
    ):
        for num_obj in range(count):
            random_num = random.randrange(free_coords_count - num_obj)
            counter = 0
            for y in range(self.MAP_Y):
                for x in range(self.MAP_X):
                    for existing_objs in itertools.chain(*args, obj_list):
                        if [x, y] in existing_objs: break
                    else:
                        if counter == random_num:
                            obj_list.append([x, y])
                            self.update_label_color(
                                self.grid_labels[y][x],
                                color
                            )
                            break
                        counter += 1
                else: continue
                break

    def update_label_color(self, label, color):
        palette = label.palette()
        palette.setColor(QPalette.Window, QColor(color))
        label.setPalette(palette)

    def draw_current_tick(self, pcolor='red'):
        for y in range(self.MAP_Y):
            for x in range(self.MAP_X):
                label = self.grid_labels[y][x]
                label.setText('   ')
                if [x, y] in self.mines:
                    self.update_label_color(label, 'blue')
                elif [x, y] in self.zombies:
                    self.update_label_color(label, 'pink')
                else:
                    self.update_label_color(label, 'lime')

        player_label = self.grid_labels[self.player_y][self.player_x]
        player_label.setText('P')
        self.update_label_color(player_label, pcolor)

    def move_zombies(self):
        for i, pos in enumerate(self.zombies):
            x = pos[0]
            y = pos[1]
            new_pos = [pos[0], pos[1]]
            n = abs(self.player_x - x)
            m = abs(self.player_y - y)
            if (
                n <= self.ZOMBIE_RANGE and
                m <= self.ZOMBIE_RANGE
            ):
                if n > m:
                    if x < self.player_x:
                        # self.zombies[i][0] += 1
                        new_pos[0] += 1
                    else:
                        # self.zombies[i][0] -= 1
                        new_pos[0] -= 1
                elif n < m:
                    if y < self.player_y:
                        # self.zombies[i][1] += 1
                        new_pos[1] += 1
                    else:
                        # self.zombies[i][1] -= 1
                        new_pos[1] -= 1
                else:
                    x_or_y = random.randint(0, 1)
                    if x_or_y == 0:
                        d = self.player_x - x
                        d /= abs(d)
                        # self.zombies[i][0] += d
                        new_pos[0] += d
                    else:
                        d = self.player_y - y
                        d /= abs(d)
                        # self.zombies[i][1] += d
                        new_pos[1] += d
            else:
                direction = random.choice((-1, 1))
                if random.randint(0, 1) == 0:
                    new_x = x + direction
                    if new_x < 0: new_x = x + 1
                    elif new_x > self.MAP_X - 1: new_x = x - 1
                    # self.zombies[i][0] = new_x
                    new_pos[0] = new_x
                else:
                    new_y = y + direction
                    if new_y < 0: new_y = y + 1
                    elif new_y > self.MAP_Y - 1: new_y = y - 1
                    # self.zombies[i][1] = new_y
                    new_pos[1] = new_y
            if new_pos not in self.zombies:
                self.zombies[i] = new_pos

    def game_tick_a(self):
        if self.tick_count == self.ESCAPE_TIME / self.TICK_INTERVAL:
            self.tick_count = 0
            self.tick_timer.timeout.disconnect(self.game_tick_a)
            self.tick_timer.timeout.connect(self.game_tick_c)
        else:
            self.game_tick_b()
            self.draw_current_tick()
            self.pending_move = None
            if self.tick_count % self.TICKS_TO_SECOND == 0:
                self.time_left_label.setText(f'Time to start: {(self.ESCAPE_TIME - self.tick_count * self.TICK_INTERVAL) / 1000}')

    def game_tick_b(self):
        self.tick_count += 1

        if self.pending_move:
            new_x = self.player_x + self.pending_move[0]
            new_y = self.player_y + self.pending_move[1]

            if 0 <= new_x < self.MAP_X and 0 <= new_y < self.MAP_Y:
                self.player_x, self.player_y = new_x, new_y

        if [self.player_x, self.player_y] in self.zombies:
            self.draw_current_tick(pcolor='purple')
            QMessageBox.critical(self, 'Game over', 'Killed by a zombie')
            self.close()
            return True

        if [self.player_x, self.player_y] in self.mines:
            self.draw_current_tick(pcolor='orange')
            QMessageBox.critical(self, 'Game over', 'You stepped on a mine')
            self.close()
            return True

        return False

    def game_tick_c(self):
        if self.game_tick_b(): return

        if self.tick_count % self.ZOMBIE_TICK_MODULO == 0:
            self.move_zombies()

            if [self.player_x, self.player_y] in self.zombies:
                self.draw_current_tick(pcolor='purple')
                QMessageBox.critical(self, 'Game over', 'Killed by a zombie')
                self.close()
                return

            for zombie in self.zombies:
                if zombie in self.mines:
                    self.zombies.remove(zombie)
                    self.mines.remove(zombie)

        self.draw_current_tick(pcolor='red')
        self.pending_move = None

        if self.tick_count % self.TICKS_TO_SECOND == 0:
            self.time_left_label.setText(f'Time left: {((self.TICKS_TO_WIN - self.tick_count) * self.TICK_INTERVAL) / 1000}')

        if self.tick_count == self.TICKS_TO_WIN:
            QMessageBox.information(self, 'Victory', 'You survived')
            self.close()
            return

    def keyPressEvent(self, event):
        key = event.key()
        if key in self.MOVES:
            self.pending_move = self.MOVES[key]

if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())