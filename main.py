import pygame
pygame.init()

WIDTH_INIT = 1000
HEIGHT_INIT = 900
WIDTH, HEIGHT = 800,720

screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption('Two-Player Pygame Chess!')
# These are the classic variables that we need to use for every game in 'pygame'. The 'WIDTH' and 'HEIGHT' correspond to the size of the screen that will pop up.
# The 'screen' variable is the place where we're going to draw everything that happens during the game.


# Even as the font is the same we put three different sizes. Why? Most probably for aesthetic purposes

timer = pygame.time.Clock()
fps = 60

# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
# The 'selection' variable appears to just be an arbitrary number that will change depending on what we select.
valid_moves = []

def calcular_escala():
    scale_x = screen.get_width() / WIDTH_INIT
    scale_y = screen.get_height() / HEIGHT_INIT
    return min(scale_x, scale_y)  # Escala uniforme para evitar distorsión
def escalar(valor):
    return int(valor * calcular_escala())
def cargar_imagen(file, width, height):
    image = pygame.image.load(file)
    return pygame.transform.scale(image, (escalar(width), escalar(height)))
def obtener_fuente(tamaño):
    return pygame.font.Font('freesansbold.ttf', escalar(tamaño))

SMALL_FONT = obtener_fuente(20)
MEDIUM_FONT = obtener_fuente(40)
BIG_FONT = obtener_fuente(50)

# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = cargar_imagen("images/black_queen.png", 80, 80)

black_queen_small = cargar_imagen("images/black_queen.png", 45, 45)
# While it doesn't appear as an option to tab, to link a file to the method '.load()' I just need to put the name of the folder next to a ...
# ... slash (/) and the file name and extension.

black_king = cargar_imagen("images/black_king.png", 80, 80)
black_king_small = cargar_imagen("images/black_king.png", 45, 45)

black_rook = cargar_imagen("images/black_rook.png", 80, 80)
black_rook_small = cargar_imagen("images/black_rook.png", 45, 45)


black_bishop = cargar_imagen("images/black_bishop.png", 80, 80)
black_bishop_small = cargar_imagen("images/black_bishop.png", 45, 45)


black_knight = cargar_imagen("images/black_knight.png", 80, 80)
black_knight_small = cargar_imagen("images/black_knight.png", 45, 45)


black_pawn = cargar_imagen("images/black_pawn.png", 65, 65)
black_pawn_small = cargar_imagen("images/black_pawn.png", 45, 45)


white_queen = cargar_imagen("images/white_queen.png", 80, 80)
white_queen_small = cargar_imagen("images/white_queen.png", 45, 45)


white_king = cargar_imagen("images/white_king.png", 80, 80)
white_king_small = cargar_imagen("images/white_king.png", 45, 45)


white_rook = cargar_imagen("images/white_rook.png", 80, 80)
white_rook_small = cargar_imagen("images/white_rook.png", 45, 45)


white_bishop = cargar_imagen("images/white_bishop.png", 80, 80)
white_bishop_small = cargar_imagen("images/white_bishop.png", 45, 45)


white_knight = cargar_imagen("images/white_knight.png", 80, 80)
white_knight_small = cargar_imagen("images/white_knight.png", 45, 45)


white_pawn = cargar_imagen("images/white_pawn.png", 65, 65)
white_pawn_small = cargar_imagen("images/white_pawn.png", 45, 45)

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
white_promotions = ['bishop', 'knight', 'rook', 'queen']
white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False,]

small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
black_promotions = ['bishop', 'knight', 'rook', 'queen']
black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False,]

small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables/ flashing counter
counter = 0
winner = ''
game_over = False
white_ep = (escalar(100), escalar(100))
black_ep = (escalar(100), escalar(100))
# Again, two nonsense values.
white_promote = False
black_promote = False
promo_index = 100
# Using our favorite dummy value

# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [escalar(600) - escalar(column * 200), escalar(row * 100), escalar(100), escalar(100)])
        else:
            pygame.draw.rect(screen, 'light gray', [escalar(700) - escalar(column * 200), row * escalar(100), escalar(100), escalar(100)])
        pygame.draw.rect(screen, 'gray', [0, escalar(800), WIDTH, escalar(100)])
        pygame.draw.rect(screen, 'gold', [0, escalar(800), WIDTH, escalar(100)], 5)
        pygame.draw.rect(screen, 'gold', [escalar(800), 0, escalar(200), HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(BIG_FONT.render(status_text[turn_step], True, 'black'), (escalar(20), escalar(820)))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, escalar(100) * i), (escalar(800), escalar(100) * i), 2)
            pygame.draw.line(screen, 'black', (escalar(100) * i, 0), (escalar(100) * i, escalar(800)), 2)
        screen.blit(MEDIUM_FONT.render('FORFEIT', True, 'black'), (escalar(810), escalar(830)))
        if white_promote or black_promote:
            pygame.draw.rect(screen, 'gray', [0, escalar(800), WIDTH - escalar(200), escalar(100)])
            pygame.draw.rect(screen, 'gold', [0, escalar(800), WIDTH - escalar(200), escalar(100)], 5)
            # The reason why we add the '- 200' is so we don't erase the "FORFEIT" button.
            screen.blit(BIG_FONT.render('Select Piece to Promote Pawn', True, 'black'), (escalar(20), escalar(820)))


# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * escalar(100) + escalar(22), white_locations[i][1] * escalar(100) + escalar(30)))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * escalar(100) + escalar(10), white_locations[i][1] * escalar(100) + escalar(10)))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * escalar(100) + escalar(1), white_locations[i][1] * escalar(100) + escalar(1),
                                                 escalar(100), escalar(100)], 2)
                # The 'red' argument seems to be the color that the options of the white pieces will look like. And indeed it is, as the black pieces have the same ...
                # ... functionality but with the color 'blue'.
                # That 'turn_step' has to be less than two makes me believe is so the red color will only appear during the white's turn, what I don't understand yet ...
                # ... is why 'selection' has to be equal to 'i'? We want the color to just appear once we have done the selection, and indeed works as intented, yet ...
                # ... I don't see how 'selection' could ever be equal to 'i', as at least on this function we don't ever change the value of 'selection'.

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * escalar(100) + escalar(22), black_locations[i][1] * escalar(100) + escalar(30)))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * escalar(100) + escalar(10), black_locations[i][1] * escalar(100) + escalar(10)))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * escalar(100) + escalar(1), black_locations[i][1] * escalar(100) + escalar(1),
                                                  escalar(100), escalar(100)], 2)


# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
            # It seems that we have a separate function for each piece, and indeed it makes sense that we need to pass in a 'location' which I suppose is equal to the ...
            # ... position we put our mouse in and do right click, yet we also need to provide a 'turn' argument. As the functions are called just the pieces and aren't ...
            # ... being preceded by either "black" or "white" I think 'turn' is a clever way to calculate the possible ways in which a piece can move, but only if the ...
            # ... 'turn_step' aligns with the turn of the color that actually has the right to move.
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# check king valid moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    # The arguments names in 'check_pawn()' in 'check_options()' are 'location' and 'turn' while here are 'position' and 'color', which gives power to the idea that ...
    # ... I had that the second argument checks if the piece you selected corresponds to the color that has the right to move on this turn.
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            # For what I see this corresponds to what are considered "legal moves"
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
            # This identation is necessary because while the first 'if' checks that the position in front of the pawn is available, this second one does ...
            # ... it too, but it should do it only after the first one has been checked. Why? Because knights are able to "jump" pieces, so if this second ...
            # ... 'if' and 'moves_list.append()' are not indented, a pawn can effectively jump over a knight with its double inicial step.
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # These last two 'if' statements check if it is possible for a white piece to capture a black one diagonally.
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
            # Why 2 'if' statements? Because any pawn has at most two diagonals to attack, so we need 2 'if' statements for normal capture, and 2 'if' statements ...
        # ... for "en passant" capture.
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
            # This follows the same logic that the white pieces, so we should indent this 'if' and 'moves_list.append()' too.
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        # The two 'if' statements below check for "en passant" capture.
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list



# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * escalar(100) + escalar(50), moves[i][1] * escalar(100) + escalar(50)), 5)


# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (escalar(825), escalar(5) + escalar(50) * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (escalar(925), escalar(5) + escalar(50) * i))


# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * escalar(100) + escalar(1),
                                                              white_locations[king_index][1] * escalar(100) + escalar(1), escalar(100), escalar(100)], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(SMALL_FONT.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(SMALL_FONT.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

# Check if en passant is an available move
def check_ep(old_coords, new_coords):
    if turn_step <= 1:
        index = white_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] - 1)
        # The minus is because the way we draw the game, with the white pieces on the upper side of the screen, requires that the white pieces go down.
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)
        # Precisely the opposite of what happens to the black pieces, that is why we have a plus (+) sign.
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        # The absolute value is to avoid the need to check for both the black and white pieces. Basically what this tells us is that if an enemy pawn moved ...
        # ... to pass an ally pawn, our ally pawn has the opportunity to capture it. That is why we want the value to be above 1, as if it was just one ...
        # ... we would already had the standard capture to get it out of the way.
        pass
    else:
        ep_coords = (escalar(100), escalar(100))
        # As a means to make them useless; there isn't any way for (100, 100) to occur, so the program won't crash or create any unexpected behavior.
        # But why do we make them useless? Because this function just cares of calculating a proper "en passant" possibility, so if the 'if' statement above ...
        # ... is true, then we just go at the end of the function to return the 'ep_coords', which is one square behind the captured pawn.
    return ep_coords
    # As this function works with what were the old coordinates of any given piece, by definition we also check that the "en passant" capture is only available ...
    # ... for one turn only.

def check_promotion():
    pawn_indexes = []
    # A list that contains all the locations in which the pawns are.
    white_promotion = False
    black_promotion = False
    promote_index = 100
    # A dummy value
    for i in range(len(white_pieces)):
        if white_pieces[i] == "pawn":
            pawn_indexes.append(i)
    for j in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[j]][1] == 7:
            # The 7 represents that we are at the last row of the game board (as we start with index 0), which means that our white pawn is elligible to promote.
            white_promotion = True
            promote_index = pawn_indexes[j]
            # By passing the index 'j' we ensure that the pawn that is being promoted is the correct one.
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == "pawn":
            pawn_indexes.append(i)
    for j in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[j]][1] == 0:
            # Note how in the black pieces we use the value of 0, as it represents the "top" of the board, from the black player's perspective.
            black_promotion = True
            promote_index = pawn_indexes[j]
    return white_promotion, black_promotion, promote_index

def draw_promotion():
    pygame.draw.rect(screen, 'dark gray', [escalar(800), 0, escalar(200), escalar(420)])
    if white_promote:
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (escalar(860), escalar(5) + escalar(100) * i))
            # The multiplication is just to space the pieces from one another, while the '+ 5' is just so the first piece doesn't touch the upper border.
            # As there are 4 "power pieces" to which the pawn can be promoted into, 420 pixels is more than enough space to contain all of them.
    elif black_promote:
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (escalar(860), escalar(5) + escalar(100) * i))
    pygame.draw.rect(screen, color, [escalar(800), 0, escalar(200), escalar(420)], 8)

def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // escalar(100)
    y_pos = mouse_pos[1] // escalar(100)
    # The reason why we use the '// 100' is because each of our squares is 100 width, and 100 height, so when we click over any of them we want to select ...
    # ... what is being shown in the entire 'quadrant' of that click.
    if white_promote and left_click and x_pos > 7 and y_pos < 4:
        # The reason why we're using 'x_pos > 7' is because as our table board has 8 squares as width, when we go further than 7 that means we are touching the ...
        # ... right menu, actually selecting the piece to promote.
        # The 'y_pos < 4' has the same idea, as the menu of the possible pieces to promote is just 4 pieces, that means that if we go beyond it we aren't ...
        # ... actually clicking the menu with the piece we want to select.
        white_pieces[promo_index] = white_promotions[y_pos]
        # As the images are being displayed in the same order that our list contains the pieces, when we select any of them (that is what 'y_pos' is used ...
        # ... for) we are actually giving an index for the 'white_promotions' list with the piece we want to promote into.
    elif black_promote and left_click and x_pos > 7 and y_pos < 4:
        # As both the promotions are being drawn on the same place, we don't really need to change the 'x_pos > 7' or 'y_pos < 4' statements.
        black_pieces[promo_index] = black_promotions[y_pos]




# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True

while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        # Just slightly different names from what the 'check_promotion' returns.
        # Notice how they're ordered in exactly the same way that in the 'return' statement of the 'check_promotion()' function.
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // escalar(100)
            y_coord = event.pos[1] // escalar(100)
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_ep = check_ep(white_locations[selection], click_coords)
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    # To capture (pop) the pawn that has been captured "en passant", and put him on the captured pieces.
                    if click_coords == black_ep:
                        black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_ep = check_ep(black_locations[selection], click_coords)
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    # En passant capture.
                    if click_coords == white_ep:
                        white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                        captured_pieces_black.append(white_pieces[white_piece])
                        # It is important to note that the captured piece goes on the 'captured_pieces' but with the 'black' suffix, which can be a bit ...
                        # ... confusing considerating that every other adjective in this 'if' statement block is 'white'.
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()
    # print(black_ep, white_ep)
    # This print statement allows us to see what is the location a pawn would travel if he had the option to capture "en passant". Recall that in the board ...
    # ... we start from (0,0) in the leftmost square and then move it to 7 in both directions, being the first integer the columns and the second the rows.
    pygame.display.flip()
pygame.quit()
