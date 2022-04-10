import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types/shapes


# MAIN FUNCTION OF THE PROGRAM
# -------------------------------------------------------------------------------
# Main function where this program starts execution
# programın yürütülmeye başlandığı ana işlev
def start():

    # set the dimensions of the game grid
    # oyun ızgarasının boyutları ayarlanır.
    grid_h, grid_w = 20, 12
    # set the size of the drawing canvas
    # çizim tuvalinin boyutları ayarlanır
    canvas_h, canvas_w = 40 * grid_h, 40 * (grid_w + 10)
    stddraw.setCanvasSize(canvas_w + 10, canvas_h)
    # set the scale of the coordinate system
    # kordinat sisteminin ölçeği ayarlanır
    stddraw.setXscale(-0.5, grid_w + 9.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    row_cleaned = False



    # set the dimension values stored and used in the Tetromino class
    # Tetromino sınıfında saklanan ve kullanılan boyut değerlerini ayarlayın
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w

    # create the game grid
    # oyun ızgarasını oluştur
    grid = GameGrid(grid_h, grid_w)
    # create the first tetromino to enter the game grid
    # by using the create_tetromino function defined below
    # oyun ızgarasına giren ilk tetrominoyu yaratın
    # aşağıda tanımlanan create_tetromino işlevini kullanarak
    tetro_array = [create_tetromino(grid_h,grid_w),create_tetromino(grid_h, grid_w)]
    grid.tetro_array = tetro_array
    current_tetromino = tetro_array[0]
    grid.current_tetromino = current_tetromino

    tetro_array.pop(0)
    tetro_array.append(create_tetromino(grid_h, grid_w))

    # display a simple menu before opening the game
    # by using the display_game_menu function defined below
    # oyunu açmadan önce basit bir menü göster
    # aşağıda tanımlanan display_game_menu işlevini kullanarak
    display_game_menu(grid_h, grid_w)

    # the main game loop (keyboard interaction for moving the tetromino)
    # ana oyun döngüsü (tetrominoyu hareket ettirmek için klavye etkileşimi)
    while True:
        # check user interactions via the keyboard
        # klavye aracılığıyla kullanıcı etkileşimlerini kontrol edin
        if stddraw.hasNextKeyTyped():  # kullanıcının bir tuşa basıp basmadığını kontrol edin
            key_typed = stddraw.nextKeyTyped()  # en son basılan tuş
            # if the left arrow key has been pressed
            # sol ok tuşuna basılmışsa
            if key_typed == "left":
                # move the active tetromino left by one
                # aktif tetrominoyu birer birer sola hareket ettirin
                current_tetromino.move(key_typed, grid)
                # if the right arrow key has been pressed
                # sağ ok tuşuna basılmışsa
            elif key_typed == "right":
                # move the active tetromino right by one
                # aktif tetromino'yu bir sağa hareket ettirin
                current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            # aşağı ok tuşuna basılmışsa
            elif key_typed == "down":
                # move the active tetromino down by one
                # (soft drop: causes the tetromino to fall down faster)
                # aktif tetromino'yu birer birer aşağı hareket ettirin
                # (yumuşak düşüş: tetromino'nun daha hızlı düşmesine neden olur)
                current_tetromino.move(key_typed, grid)
            elif key_typed == 'up':
                x = current_tetromino.rotate_clockwise(grid)
                if not x:
                    current_tetromino.rotate_counter_clockwise(grid)


            elif key_typed == 'left ctrl':
                x = current_tetromino.rotate_counter_clockwise(grid)
                if not x:
                    current_tetromino.rotate_clockwise(grid)


            elif key_typed == "space":
                grid.DropCurrentTetromino()

            # clear the queue of the pressed keys for a smoother interaction
            # daha sorunsuz bir etkileşim için basılan tuşların sırasını temizleyin
            stddraw.clearKeysTyped()

        # move the active tetromino down by one at each iteration (auto fall)
        # aktif tetromino'yu her yinelemede bir aşağı hareket ettirin (otomatik düşüş)
        success = current_tetromino.move("down", grid)
        grid.merge(0)
        grid.clear_rows()

        # place the active tetromino on the grid when it cannot go down anymore
        # aktif tetromino'yu artık aşağı inemediğinde ızgaraya yerleştirin
        if not success:
            # get the tile matrix of the tetromino without empty rows and columns
            # and the position of the bottom left cell in this matrix
            # tetromino'nun karo matrisini boş satırlar ve sütunlar olmadan alın
            # ve bu matristeki sol alt hücrenin konumu
            tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
            # update the game grid by locking the tiles of the landed tetromino
            # inen tetromino'nun karolarını kilitleyerek oyun ızgarasını güncelleyin
            game_over = grid.update_grid(tiles, pos)
            # end the main game loop if the game is over
            # oyun bittiyse ana oyun döngüsünü sonlandır
            if game_over:
                display_gameover_menu(grid_w + 4, grid_h + 3)

                break
            current_tetromino = tetro_array[1]
            grid.current_tetromino = current_tetromino


            # create the next tetromino to enter the game grid
            # by using the create_tetromino function defined below
            # oyun ızgarasına girmek için bir sonraki tetromino'yu oluşturun
            # aşağıda tanımlanan create_tetromino işlevini kullanarak
            tetro_array.pop(0)
            tetro_array.append(create_tetromino(grid_h, grid_w))





        # display the game grid and the current tetromino
        # oyun ızgarasını ve mevcut tetrominoyu göster
        grid.display()

    # print a message on the console when the game is over
    # oyun bittiğinde konsola bir mesaj yazdır
    print("Game over")

#def create_clear_rows(self, locked):
    #clear_rows = GameGrid(create_clear_rows(self, locked))
    #return create_clear_rows()

# Function for creating random shaped tetrominoes to enter the game grid
# Oyun ızgarasına girmek için rastgele şekilli tetrominolar oluşturma işlevi
def create_tetromino(grid_height, grid_width):
    # type (shape) of the tetromino is determined randomly
    # tetromino tipi (şekli) rastgele belirlenir
    tetromino_types = ['I', 'O', 'Z', 'T', 'L', 'J', 'S']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    # create and return the tetromino
    # tetromino'yu oluştur ve döndür
    tetromino = Tetromino(random_type)
    return tetromino
# Function for displaying a simple menu before starting the game
# Oyuna başlamadan önce basit bir menüyü görüntüleme işlevi
def display_game_menu(grid_height, grid_width):
    # colors used for the menu
    # menü için kul lanılan renk
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background canvas to background_color
    # arka plan tuvalini background_color olarak temizle
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    # bu python kod dosyasının yerleştirildiği dizini alın
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    # görüntü dosyasının yolu
    img_file = current_dir + "/images/menu_image.png"
    # center coordinates to display the image
    # resmi görüntülemek için merkez koordinatları
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # image is represented using the Picture class
    # resim, Resim sınıfı kullanılarak temsil edilir
    image_to_display = Picture(img_file)
    # display the image
    # resmi göster
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    # oyunu başlat düğmesinin boyutları
    button_w, button_h = grid_width - 1.5, 2
    # coordinates of the bottom left corner of the start game button
    # oyunu başlat düğmesinin sol alt köşesinin koordinatları
    button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
    # display the start game button as a filled rectangle
    # oyunu başlat düğmesini içini dolu bir dikdörtgen olarak göster
    stddraw.setPenColor(button_color)
    stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
    # display the text on the start game button
    # oyunu başlat düğmesindeki metni göster
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(25)
    stddraw.setPenColor(text_color)
    text_to_display = "Click Here to Start the Game"
    stddraw.text(img_center_x, 5, text_to_display)
    # menu interaction loop
    # menü etkileşim döngüsü
    while True:
        # display the menu and wait for a short time (50 ms)
        # menüyü görüntüleyin ve kısa bir süre bekleyin (50 ms)
        stddraw.show(50)
        # check if the mouse has been left-clicked on the button
        # farenin düğmeye sol tıklanıp tıklanmadığını kontrol edin
        if stddraw.mousePressed():
            # get the x and y coordinates of the location at which the mouse has
            # most recently been left-clicked
            # farenin bulunduğu konumun x ve y koordinatlarını alın
            # en son sol tıklandı
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # check if these coordinates are inside the button
            # bu koordinatların düğmenin içinde olup olmadığını kontrol edin
            if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
                if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
                    break  # break the loop to end the method and start the game
                    # yöntemi sonlandırmak ve oyunu başlatmak için döngüyü kırın
def display_gameover_menu(grid_height, grid_width):
    # colors used for the menu
    # menü için kul lanılan renk
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    # clear the background canvas to background_color
    # arka plan tuvalini background_color olarak temizle
    stddraw.clear(background_color)
    # get the directory in which this python code file is placed
    # bu python kod dosyasının yerleştirildiği dizini alın
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # path of the image file
    # görüntü dosyasının yolu
    img_file = current_dir + "/images/gameover.png"
    # center coordinates to display the image
    # resmi görüntülemek için merkez koordinatları
    img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
    # image is represented using the Picture class
    # resim, Resim sınıfı kullanılarak temsil edilir
    image_to_display = Picture(img_file)
    # display the image
    # resmi göster
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    # dimensions of the start game button
    # oyunu başlat düğmesinin boyutları

    # display the text on the start game button
    # oyunu başlat düğmesindeki metni göster
    while True:
        # display the menu and wait for a short time (50 ms)
        # menüyü görüntüleyin ve kısa bir süre bekleyin (50 ms)
        stddraw.show(50)

    # menu interaction loop
    # menü etkileşim döngüsü


# start() function is specified as the entry point (main function) from which
# the program starts execution
# start() işlevi, giriş noktası (ana işlev) olarak belirtilir.
# program yürütmeye başlar
if __name__ == '__main__':
    start()
