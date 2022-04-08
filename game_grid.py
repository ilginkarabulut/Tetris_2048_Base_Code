import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import random
from tetromino import Tetromino

# Class used for modelling the game grid
from tetromino import Tetromino


class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    # Verilen argümanlara dayalı oyun ızgarasını oluşturmak için yapıcı
    def __init__(self, grid_h, grid_w):

        # set the dimensions of the game grid as the given arguments
        # oyun ızgarasının boyutlarını verilen argümanlar olarak ayarlayın
        self.grid_height = grid_h
        self.grid_width = grid_w

        # create a tile matrix to store the tiles landed onto the game grid
        # oyun ızgarasına konan karoları depolamak için bir karo matrisi oluşturun
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        # şu anda oyun ızgarasında taşınmakta olan tetromino'yu oluşturun
        self.current_tetromino = None
        # the game_over flag shows whether the game is over or not
        # game_over bayrağı oyunun bitip bitmediğini gösterir
        self.game_over = False
        # set the color used for the empty grid cells
        # boş ızgara hücreleri için kullanılan rengi ayarlayın
        self.empty_cell_color = Color(42, 69, 99)
        # set the colors used for the grid lines and the grid boundaries
        # ızgara çizgileri ve ızgara sınırları için kullanılan renkleri ayarlayın
        self.line_color = Color(0, 100, 200)
        self.boundary_color = Color(0, 100, 200)
        # thickness values used for the grid lines and the boundaries
        # ızgara çizgileri ve sınırlar için kullanılan kalınlık değerleri
        self.line_thickness = 0.002
        self.box_thickness = 10 * self.line_thickness

    # Method used for displaying the game grid
    # Oyun tablosunu görüntülemek için kullanılan yöntem
    def display(self):





        # clear the background to empty_cell_color
        # boş_hücre_renk için arka planı temizle
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        # oyun ızgarasını çiz
        self.draw_grid()
        # draw the current/active tetromino if it is not None (the case when the
        # game grid is updated)
        # Yok değilse mevcut/aktif tetrominoyu çizin (
        # oyun kılavuzu güncellendi)
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        # oyun ızgarasının etrafına bir kutu çizin
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = 250 ms
        # bir duraklama süresi ile elde edilen çizimi göster = 250 ms
        stddraw.show(250)

    # Method for drawing the cells and the lines of the game grid
    # Oyun ızgarasının hücrelerini ve çizgilerini çizme yöntemi

    def draw_grid(self):
        self.draw_leaderboard()

        # for each cell of the game grid
        # oyun ızgarasının her hücresi için
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                # ızgara hücresi bir döşeme tarafından işgal edilmişse döşemeyi çizin
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))
        # draw the inner lines of the grid
        # ızgaranın iç çizgilerini çizin
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        # oyun ızgarası için x ve y aralıkları
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    # Oyun ağının etrafındaki sınırları çizme yöntemi
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    def draw_leaderboard(self):
        pos_x, pos_y = -0.5, -0.5
        GRAY = Color(128, 128, 128)
        stddraw.setPenColor(GRAY)
        stddraw.rectangle(pos_x + self.grid_width, pos_y, self.grid_width, self.grid_height)
        stddraw.filledRectangle(pos_x + self.grid_width, pos_y, self.grid_width, self.grid_height)

    def clear_rows(self, locked):
        increase = 0
        for i in range(len(self) - 1, -1, -1):  # start check the grid backwards
            rows = self[i]  # get last row
            if (0, 0, 0) not in rows:  # not empty spaces
                increase += 1
                # add positions to remove from locked
                index = i  # row index will be constant
                for j in range(len(rows)):
                    try:
                        del locked[(j, i)]  # delete locked element in the bottom row
                    except ValueError:
                        continue

            if increase > 0:
                for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
                    x, y = key
                    if y < index:
                        new_key = (x, y + increase)
                        locked[new_key] = locked.pop(key)

            return increase

    def DropCurrentTetromino(self):
        while self.current_tetromino.can_be_moved("down", self):
            self.current_tetromino.bottom_left_cell.y -= 1

    # Method used for checking whether the grid cell with given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # considering newly entered tetrominoes to the game grid that may have
        # tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    def clear_rows(grid, locked):
        increase = 0
        for i in range(len(grid) - 1, -1, -1):  # start check the grid backwards
            rows = grid[i]  # get last row
            if (0, 0, 0) not in rows:  # not empty spaces
                increase += 1
                # add positions to remove from locked
                index = i  # row index will be constant
                for j in range(len(rows)):
                    try:
                        del locked[(j, i)]  # delete locked element in the bottom row
                    except:
                        continue

            if increase > 0:
                for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                    x, y = key
                    if y < index:
                        new_key = (x, y + increase)
                        locked[new_key] = locked.pop(key)

            return increase

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Method that locks the tiles of the landed tetromino on the game grid while
    # checking if the game is over due to having tiles above the topmost grid row.
    # The method returns True when the game is over and False otherwise.
    def update_grid(self, tiles_to_lock, blc_position):
        # necessary for the display method to stop displaying the tetromino
        self.current_tetromino = None
        # lock the tiles of the current tetromino (tiles_to_lock) on the game grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each tile onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is above the game grid
                    else:
                        self.game_over = True
        # return the game_over flag
        return self.game_over
