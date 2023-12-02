import pygame
import numpy as np
import pandas as pd

current_game_id = 0
games = {}


# Create board
def create_board():
    board = [[0 for _ in range(7)] for _ in range(6)]
    return board


# Check that column isn't full
def col_not_full(board, col):
    return board[5][col] == 0  # true if column isn't full


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


# create a node class for the linked list
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


# create a linked list class to store the moves
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


class TreeNode:
    def __init__(self, board, col=None, score=0):
        self.board = board
        self.children = []
        self.col = col  # The column that led to this board state
        self.score = score  # The score of this board state

    def add_child(self, child_node):
        self.children.append(child_node)


def build_tree(current_node, depth, player):
    if depth == 0:
        return

    for col in range(7):
        if col_not_full(current_node.board, col):
            new_board = [row[:] for row in current_node.board]
            row = row_finder(new_board, col)
            place_piece(new_board, row, col, player)
            child_node = TreeNode(new_board, col)
            current_node.add_child(child_node)
            next_player = 2 if player == 1 else 1
            build_tree(child_node, depth - 1, next_player)


def score_position(board, player):
    score = 0  # Initialize score

    ## Score center column
    center_column = [board[i][3] for i in range(6)] 
    center_count = center_column.count(player)  
    score += center_count * 3  

    ## Score Horizontal
    for r in range(6): 
        row = board[r] 
        for c in range(4): 
            window = row[c:c+4] 
            score += evaluate_window(window, player)  

    ## Score Vertical
    for c in range(7):  
        column = [board[r][c] for r in range(6)] 
        for r in range(3): 
            window = column[r:r+4]  
            score += evaluate_window(window, player)  

    ## Score Positive Sloped Diagonals
    for r in range(3): 
        for c in range(4): 
            window = [board[r+i][c+i] for i in range(4)] 
            score += evaluate_window(window, player)  

    ## Score Negative Sloped Diagonals
    for r in range(3, 6): 
        for c in range(4):  
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)  

    return score  

def evaluate_window(window, player):
    score = 0 
    opp_player = 1 if player == 2 else 2  

    if window.count(player) == 4:
        score += 100  
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 10  
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 5  

    if window.count(opp_player) == 3 and window.count(0) == 1:
        score -= 8 

    return score  



def cpu_move(board, game_id):

    root = TreeNode(board)
    build_tree(root, 3, 2) # depth of decision tree
    max_score = float('-inf')
    best_col = None

    for child in root.children:
        child.score = score_position(child.board, 2)  
        if child.score > max_score:
            max_score = child.score
            best_col = child.col

    row = row_finder(board, best_col)
    place_piece(board, row, best_col, 2)
    add_move(game_id, best_col)
    game = check_winning_move(board, row, best_col, 2)
    return game

def check_draw(board):
    for row in board:
        if 0 in row:
            return False 
    return True  # All spots are filled, the game is a draw



# Connect 4
def play_game(colors, names, player1_score, player2_score, cpu):
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
    screen.blit(welcome_text, ((900 - welcome_text.get_width()) // 2, 35))
    score_text = score_font.render(f"{names[0]}'s score: {player1_score}", True, colors[4])
    screen.blit(score_text, (20, 740))
    score_text = score_font.render(f"{names[1]}'s score: {player2_score}", True, colors[4])
    screen.blit(score_text, (880 - score_text.get_width(), 740))

    draw_board(board, colors, screen)
    pygame.display.update()

    while not game:
        for event in pygame.event.get():
            print(event)
            if cpu and player == 2:
                game = cpu_move(board, game_id)  # CPU always plays if player didn't win
                draw_board(board, colors, screen)
                player = 2 if player == 1 else 1
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, colors[3], (0, 0, 900, 80))
                col = event.pos[0] // 100
                col -= 1
                if col < 0 or col > 6:
                    continue
                if col_not_full(board, col):
                    row = row_finder(board, col)
                    place_piece(board, row, col, player)
                    add_move(game_id, col)
                    game = check_winning_move(board, row, col, player)
                    if not game:
                            game= 'draw' if check_draw(board) else None                   
                    draw_board(board, colors, screen)
                    player = 2 if player == 1 else 1
            if game:
                pygame.draw.rect(screen, colors[3], (0, 705, 900, 100))
                pygame.draw.rect(screen, colors[3], (0, 0, 900, 80))

                if game == 'draw':
                    draw_text = win_font.render("Game is a draw!", True, colors[4])
                    screen.blit(draw_text, ((900 - draw_text.get_width()) // 2, 35))
                else:
                    winner_name = names[0] if player == 2 else names[1]
                    loser_name = names[1] if player == 2 else names[0]
                    set_game_result(game_id, winner_name, loser_name)



                    win_text = win_font.render(f"The winner is Player {winner_name}!", True, colors[4])
                    screen.blit(win_text, ((900 - win_text.get_width()) // 2, 35))

                  # Update player scores
                    if game == 'draw':
                        player1_score += 1
                        player2_score += 1
                    elif player == 1:
                        player1_score += 1
                    else:
                        player2_score += 1

                    # Display updated scores
                    score_text = score_font.render(f"{names[0]}'s score: {player1_score}", True, colors[4])
                    screen.blit(score_text, (20, 740))
                    score_text = score_font.render(f"{names[1]}'s score: {player2_score}", True, colors[4])
                    screen.blit(score_text, (880 - score_text.get_width(), 740))

                pygame.display.update()
                pygame.time.wait(3000)
                pygame.quit()
                break

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
    cpu_mode = int(input("Choose game mode (1 for 2 players, 2 for playing against virtual player): ")) == 2
    player1_score = 0
    player2_score = 0

    player1 = input("Enter player 1's name: ").lower()
    cpu = None  
    if cpu_mode:
        cpu = True
        names = [player1, 'CPU']
    else:
        player2 = input("Enter player 2's name: ").lower()
        names = [player1, player2]
    player1_score, player2_score = play_game(colors, names, player1_score, player2_score, cpu_mode)

    while True:
        print("\n\nMain menu:")
        print("  1. Play again \n  2. Replay game \n  3. Show leaderboard \n  4. Player score \n  5. Exit")
        print()
        choice = int(input("Choose an option from the main menu: "))

        if choice == 1:
            same_players = input("\nAre the same players playing? (y/n): ")
            if same_players == "n":
                cpu = input("Choose game mode (1 for 2 players, 2 for playing aginst virtual player): ")
                player1 = (input("Enter player 1's name: ")).lower()

                if cpu:
                    names = [player1, 'CPU']
                else:
                    player2 = (input("Enter player 2's name: ")).lower()
                    names = [player1, player2]

            player1_score, player2_score = play_game(colors, names, player1_score, player2_score, cpu)

        elif choice == 2:
            print("List of games: ")
            for idx, game_details in games.items():
                print(
                    f" - Game number: {idx}\n     Winner: {game_details['winner']}\n     Loser: {game_details['loser']}\n")

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
