import pygame
import numpy as np
import pandas as pd

current_game_id = 0
games = {}


# Create board
def create_board():
    board = np.zeros((6, 7))
    return board


# Check that column isn't full
def col_full(board, col):
    full = (board[5][col] == 0)  # true if column isn't full
    return full


# Find row
def row_finder(board, col):
    for row in range(6):
        if board[row][col] == 0:
            return row


# Place piece in correct row and column
def place_piece(board, row, col, player):
    board[row][col] = player



# Check that no 4 in a row
def check_winning_move(board, row, col, player):
    # check horizontal
    for i in range(4):
        if board[row][i] == player and board[row][i + 1] == player and \
                board[row][i + 2] == player and board[row][i + 3] == player:
            return True

    # check vertical
    for i in range(3):
        if board[i][col] == player and board[i + 1][col] == player and \
                board[i + 2][col] == player and board[i + 3][col] == player:
            return True

    # check positive diagonal
    for i in range(4):
        for j in range(3):
            if board[j][i] == player and board[j + 1][i + 1] == player and \
                    board[j + 2][i + 2] == player and board[j + 3][i + 3] == player:
                return True

    # check negative diagonal
    for i in range(4):
        for j in range(3, 6):
            if board[j][i] == player and board[j - 1][i + 1] == player and \
                    board[j - 2][i + 2] == player and board[j - 3][i + 3] == player:
                return True

    return False


# Function to draw the board
def draw_board(board, colors, screen):
    for col in range(7):
        for row in range(6):
            pygame.draw.rect(screen, colors[2], ((col + 1) * 100, (row + 1) * 100, 100, 100))

    for col in range(7):
        for row in range(6):
            if board[row][col] == 1:
                pygame.draw.circle(screen, colors[0], (50 + (col + 1) * 100, 650 - row * 100), 35)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, colors[1], (50 + (col + 1) * 100, 650 - row * 100), 35)
            else:
                pygame.draw.circle(screen, colors[4], (50 + (col + 1) * 100, 650 - row * 100), 35)

    pygame.display.update()



#create a node class for the linked list
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


#create a linkest list class to store the moves
class LinkedList:
    def __init__(self):
        self.head = None

    def append_node(self, move):
        new_node = Node(move)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def pop_first_node(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        return data

    def iterate(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result



# Creates dictionary for game
def start_new_game():
    global current_game_id
    current_game_id += 1

    games[current_game_id] = {
        'moves': LinkedList(),
        'winner': None,
        'loser': None
    }
    return current_game_id


# Sets the winner and loser in dictionary
def set_game_result(game_id, winner_name, loser_name):
    if game_id in games:
        games[game_id]['winner'] = winner_name
        games[game_id]['loser'] = loser_name
    else:
        print(f"Game {game_id} not found.")


# Adds move to linked list
def add_move(game_id, move):
    if game_id in games:
        games[game_id]['moves'].append_node(move)
    else:
        print(f"Game {game_id} not found.")


# Game replay
def game_replay(game_id, colors):
    pygame.init()

    screen = pygame.display.set_mode((900, 800))
    pygame.display.set_caption('Connect 4')

    score_font = pygame.font.SysFont(None, 30)

    score_text = score_font.render(f"Winner: {games[game_id]['winner']}", True, colors[4])
    screen.blit(score_text, (20, 740))
    score_text = score_font.render(f"Loser: {games[game_id]['loser']}", True, colors[4])
    screen.blit(score_text, (880 - score_text.get_width(), 740))

    board = create_board()
    player = 1
    pygame.display.update()

    moves = LinkedList()
    for item in games[game_id]['moves'].iterate():
        moves.append_node(item)

    while moves.head is not None:
        col = moves.pop_first_node()
        row = row_finder(board, col)
        place_piece(board, row, col, player)
        draw_board(board, colors, screen)
        pygame.time.wait(1000)
        pygame.display.update()
        player = 2 if player == 1 else 1

    pygame.time.wait(1000)
    pygame.quit()

#With CPU
def cpu_move(board, game_id):
    
    valid_moves = []
    for col in range(7):
        if not col_full(board, col):
            continue
        valid_moves.append(col)

    cpu_col = np.random.choice(valid_moves)
    row = row_finder(board, col)
    place_piece(board, row, col, 2)
    add_move(game_id, col)
    game = check_winning_move(board, row, col, 2)

    return cpu_col

#Connect 4 w cpu
def play_game_with_cpu(colors, names, player1_score, player2_score):
    game = False
    player = 1
    board = create_board()
    game_id = start_new_game()

    # Initialize Pygame
    pygame.init()

    screen = pygame.display.set_mode((900, 800))
    pygame.display.set_caption('Connect 4')

    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 30)
    win_font = pygame.font.SysFont(None, 40)

    welcome_text = font.render("Welcome to Connect 4!", True, colors[4])
    screen.blit(welcome_text, ((900 - welcome_text.get_width())//2, 35))
    score_text = score_font.render(f"{names[0]}'s score: {player1_score}", True, colors[4])
    screen.blit(score_text, (20, 740))
    score_text = score_font.render(f"{names[1]}'s score: {player2_score}", True, colors[4])
    screen.blit(score_text, (880 - score_text.get_width(), 740))

    draw_board(board, colors, screen)
    pygame.display.update()

    while not game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, colors[3], (0, 0, 900, 80))
                col = event.pos[0] // 100
                col -= 1
                if col < 0 or col > 6:
                    continue
                if col_full(board, col):
                    row = row_finder(board, col)
                    place_piece(board, row, col, player)
                    add_move(game_id, col)
                    game = check_winning_move(board, row, col, player)
                    cpu_move(board, game_id) # CPU always plays if player didn't win
                else:
                    pygame.time.wait(1000)
                    draw_board(board, colors, screen)
                    continue

                draw_board(board, colors, screen)
                if game:
                    pygame.draw.rect(screen, colors[3], (0, 705, 900, 100))
                    pygame.draw.rect(screen, colors[3], (0, 0, 900, 80))


        score_text = score_font.render(f"{names[0]}'s score: {player1_score}", True, colors[4])
        screen.blit(score_text, (20, 740))
        score_text = score_font.render(f"{names[1]}'s score: {player2_score}", True, colors[4])
        screen.blit(score_text, (880 - score_text.get_width(), 740))
        win_text = win_font.render(f"The winner is Player {names[player-1]}!", True, colors[4])
        screen.blit(win_text, ((900 - win_text.get_width())//2, 35))

        winner_name = names[player-1]
        loser_name = names[1] if player == 1 else names[0]
        set_game_result(game_id, winner_name, loser_name)
        print(f"Player {winner_name} is the winner!")

        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        break
    else:

                cpu_col = cpu_move(board)
                row = row_finder(board, cpu_col)
                place_piece(board, row, cpu_col, player)
                add_move(game_id, cpu_col)
                game = check_winning_move(board, row, cpu_col, player)

    return player1_score, player2_score


# Connect-4
def play_game(colors, names, player1_score, player2_score):
    game = False
    player = 1
    board = create_board()
    game_id = start_new_game()

    # Initialize Pygame
    pygame.init()

    screen = pygame.display.set_mode((900, 800))
    pygame.display.set_caption('Connect 4')

    font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont(None, 30)
    win_font = pygame.font.SysFont(None, 40)

    welcome_text = font.render("Welcome to Connect 4!", True, colors[4])
    screen.blit(welcome_text, ((900 - welcome_text.get_width())//2, 35))
    score_text = score_font.render(f"{names[0]}'s score: {player1_score}", True, colors[4])
    screen.blit(score_text, (20, 740))
    score_text = score_font.render(f"{names[1]}'s score: {player2_score}", True, colors[4])
    screen.blit(score_text, (880 - score_text.get_width(), 740))

    draw_board(board, colors, screen)
    pygame.display.update()

    while not game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, colors[3], (0, 0, 900, 80))
                col = event.pos[0] // 100
                col -= 1
                if col < 0 or col > 6:
                    continue
                if col_full(board, col):
                    row = row_finder(board, col)
                    place_piece(board, row, col, player)
                    add_move(game_id, col)
                    game = check_winning_move(board, row, col, player)
                else:
                    pygame.time.wait(1000)
                    draw_board(board, colors, screen)
                    continue

                draw_board(board, colors, screen)
                if game:
                    pygame.draw.rect(screen, colors[3], (0, 705, 900, 100))
                    pygame.draw.rect(screen, colors[3], (0, 0, 900, 80))

                    if player == 1:
                        player1_score += 1
                    else:
                        player2_score += 1

                    score_text = score_font.render(f"{names[0]}'s score: {player1_score}", True, colors[4])
                    screen.blit(score_text, (20, 740))
                    score_text = score_font.render(f"{names[1]}'s score: {player2_score}", True, colors[4])
                    screen.blit(score_text, (880 - score_text.get_width(), 740))
                    win_text = win_font.render(f"The winner is Player {names[player-1]}!", True, colors[4])
                    screen.blit(win_text, ((900 - win_text.get_width())//2, 35))

                    winner_name = names[player-1]
                    loser_name = names[1] if player == 1 else names[0]
                    set_game_result(game_id, winner_name, loser_name)
                    print(f"Player {winner_name} is the winner!")

                    pygame.display.update()
                    pygame.time.wait(3000)
                    pygame.quit()
                    break
                else:
                    player = 2 if player == 1 else 1

    return player1_score, player2_score


# Counts wins and loses of player
def find_games_by_player(player_name):
    won_games = []
    lost_games = []
    for game_id, game_data in games.items():
        if game_data['winner'] == player_name:
            won_games.append(game_id)
        elif game_data['loser'] == player_name:
            lost_games.append(game_id)
    return won_games, lost_games


# Creates the leaderboard
def leaderboard():
    data = []
    wins = {}
    losses = {}

    # Count wins and losses
    for game_id, game_info in games.items():
        winner = game_info.get('winner')
        loser = game_info.get('loser')

        if winner:
            wins[winner] = wins.get(winner, 0) + 1
        if loser:
            losses[loser] = losses.get(loser, 0) + 1

    players = set(wins.keys()).union(losses.keys())
    for player in sorted(players, key=lambda x: wins.get(x, 0) - losses.get(x, 0), reverse=True):
        won = wins.get(player, 0)
        lost = losses.get(player, 0)
        net_win = won - lost
        data.append([player, won, lost, net_win])

    columns = ['Player', 'Wins', 'Losses', 'Net Wins']
    df = pd.DataFrame(data, columns=columns)
    df.index = range(1, len(df) + 1)
    return df


def main():
    colors = [(255, 0, 0), (255, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)]
    game_mode = input("Choose game mode (1 for 2 players, 2 for playing aginst virtual player): ")

    if game_mode == "1":
        player1 = (input("Enter player 1's name: ")).lower()
        player2 = (input("Enter player 2's name: ")).lower()
        names = [player1, player2]
        player1_score, player2_score = play_game(colors, names, player1_score, player2_score)       


    elif game_mode == "2":
        player1 = (input("Enter player 1's name: ")).lower()
        names = [player1, "cpu"]
        player1_score, player2_score = play_game_with_cpu(colors, names, player1_score, player2_score)


    while True:
        print("\n\nMain menu:")
        print("  1. Play again \n  2. Replay game \n  3. Show leaderboard \n  4. Player score \n  5. Exit")
        print()
        choice = int(input("Choose an option from the main menu: "))

        if choice == 1:
            same_players = input("\nAre the same players playing? (y/n): ")
            if same_players == "n":
                game_mode = input("\nChoose game mode (1 for 2 players, 2 for playing aginst virtual player): ")

                if game_mode == "1":
                    player1 = (input("Enter player 1's name: ")).lower()
                    player2 = (input("Enter player 2's name: ")).lower()
                    print()
                    names = [player1, player2]
                    player1_score, player2_score = play_game(colors, names, player1_score, player2_score)       


                elif game_mode == "2":
                    player1 = (input("Enter player 1's name: ")).lower()
                    names = [player1, "cpu"]
                    player1_score, player2_score = play_game_with_cpu(colors, names, player1_score, player2_score)

            if game_mode == "1":
                player1_score, player2_score = play_game(colors, names, player1_score, player2_score)
            else:
                player1_score, player2_score = play_game_with_cpu(colors, names, player1_score, player2_score)

        elif choice == 2:
            print("List of games: ")
            for idx, game_details in games.items():
                print(f" - Game number: {idx}\n     Winner: {game_details['winner']}\n     Loser: {game_details['loser']}\n")

            number = int(input("Enter game number: "))
            while number not in games:
                number = int(input("Enter game number: "))

            game_replay(number, colors)

        elif choice == 3:
            df = leaderboard()
            print(df)

        elif choice == 4:
            player_name = (input("Enter name of player: ")).lower()
            wins, loses = find_games_by_player(player_name)
            print(f" - Player name: {player_name}\n     Number of wins: {wins}\n     Number of loses: {loses}\n")

        elif choice == 5:
            break

        else:
            choice = int(input("Choose an option from the main menu: "))


main()