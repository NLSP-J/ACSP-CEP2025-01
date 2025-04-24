import random, time
import asyncio

word_list = ["range", "lucas","yboxu","place","earth","never","tenor","kiran","anson","yuxin","debug","scare","brace","hunts","cried","issue","sigma","drugs","arsen","avoid","fatal","voice","chair","court","royal","click","curve","table","brief","fired","screen","tough","ought"]
word = random.choice(word_list)

import pygame as pg
pg.init()

clock = pg.time.Clock()
start = pg.time.get_ticks()
win_width = 1000
win_height = 700
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Guess The Word')

white = (0, 0, 0)
black = (229, 228, 226)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)

font = pg.font.Font(None, 70)

game_board = [[' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ']]


count = 0
letters = 0

game_over = False
running = True

def draw_board():
    global clock
    global game_over
    for col in range(5):
        for row in range(6):
            square = pg.Rect(col * 100 + 12, row * 100 + 12, 75, 75)
            pg.draw.rect(screen, white, square, width = 2)
            letter_text = font.render(game_board[row][col], True, gray)
            screen.blit(letter_text, (col * 100 + 30, row * 100 + 30))
    rectangle = pg.Rect(5, count * 100 + 5, win_width - 10, 90)
    pg.draw.rect(screen, green, rectangle, width = 2)
    if game_over == False:
        text = f'Time: {clock/1000}'
        text = font.render(text, 5, white)
        screen.blit(text, (win_width - 630, win_height - 60))

def check_match():
    global game_over
    for col in range(5):
        for row in range(6):    
            highlight = pg.Rect(col * 100 + 12, row * 100 + 12, 75, 75)
            if word[col] == game_board[row][col] and count > row:
                pg.draw.rect(screen, green, highlight)
            elif game_board[row][col] in word and count > row:
                pg.draw.rect(screen, yellow, highlight)

    for row in range(6):
        guess = ''.join(game_board[row])
        if guess == word and row < count:
            game_over = True
    

def draw_win():
    global game_over
    if count == 6:
        game_over = True
        text = font.render('Game Over!', True, white)
        screen.blit(text, (15, 610))

    if game_over and count < 6:
        text = font.render('Good Job!', True, white)
        screen.blit(text, (15, 610))
        clock = pg.time.get_ticks()
        duration = (clock - start) / 1000
        text = font.render(f"Your high score is {duration} secs!", 5, white)
        screen.blit(text, (win_width - 700, win_height - 60))

async def main():
    global running, count, letters, game_over, game_board, word, word_list, clock
    word = random.choice(word_list)
    while running:
        clock = pg.time.get_ticks()
        if clock>=30001:
            break
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.TEXTINPUT and letters < 5 and not game_over:
                entry = event.text
                if entry != ' ':
                    game_board[count][letters] = entry
                    letters += 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE and letters > 0:
                    game_board[count][letters - 1] = ' '
                    letters -= 1

                if event.key == pg.K_SPACE and not game_over:
                    count += 1
                    letters = 0
                
                if event.key == pg.K_SPACE and game_over:
                    count = 0
                    letters = 0
                    game_over = False
                    word = random.choice(word_list)
                    game_board = [[' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ']]

            
        screen.fill(black)
        check_match()
        draw_board()
        draw_win()
        pg.display.update()
        if game_over:
          time.sleep(2)
          break
        await asyncio.sleep(0)

asyncio.run(main())
