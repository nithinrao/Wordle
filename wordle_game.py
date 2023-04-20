import sys
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_BACKSPACE, K_RETURN

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
CELL_SIZE = 50
MARGIN = 10
LETTER_FONT_SIZE = 25
RESULT_FONT_SIZE = 20
TEXT_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
INPUT_COLOR = (200, 200, 200)
BUTTON_COLOR = (100, 100, 255)
MSG_BOX_HEIGHT = 100

# Initialize Pygame
pygame.init()

# Fonts
LETTER_FONT = pygame.font.Font(None, LETTER_FONT_SIZE)
RESULT_FONT = pygame.font.Font(None, RESULT_FONT_SIZE)

def choose_word(words_list):
    return random.choice(words_list)

def compare_words(word, guess):
    correct_position = [i for i in range(4) if guess[i] == word[i]]
    correct_letters = [i for i in range(4) if guess[i] != word[i] and guess[i] in word]

    return correct_position, correct_letters


def draw_grid(screen, guesses, results):
    for i, guess in enumerate(guesses):
        for j, letter in enumerate(guess):
            cell_rect = pygame.Rect(j * (CELL_SIZE + MARGIN), i * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)

            if i < len(results):
                correct_position, correct_letters = results[i]

                if j in correct_position:
                    pygame.draw.rect(screen, (0, 255, 0), cell_rect)  # Green for correct position
                elif j in correct_letters:
                    pygame.draw.rect(screen, (255, 255, 0), cell_rect)  # Yellow for correct letter in the wrong position
                else:
                    pygame.draw.rect(screen, BG_COLOR, cell_rect)

            else:
                pygame.draw.rect(screen, BG_COLOR, cell_rect)

            pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)
            letter_render = LETTER_FONT.render(letter.upper(), True, TEXT_COLOR)
            letter_rect = letter_render.get_rect(center=cell_rect.center)
            screen.blit(letter_render, letter_rect)



def draw_results(screen, results):
    for i, result in enumerate(results):
        result_render = RESULT_FONT.render(result, True, TEXT_COLOR)
        result_rect = result_render.get_rect(midleft=((4 * (CELL_SIZE + MARGIN)), (i * (CELL_SIZE + MARGIN)) + CELL_SIZE // 2))
        screen.blit(result_render, result_rect)

def custom_text_input(screen, text):
    input_rect = pygame.Rect(0, 0, 4 * (CELL_SIZE + MARGIN), CELL_SIZE)
    input_rect.topleft = (0, 6 * (CELL_SIZE + MARGIN))  # Fixed position for the input box
    pygame.draw.rect(screen, INPUT_COLOR, input_rect)
    pygame.draw.rect(screen, (0, 0, 0), input_rect, 1)

    input_render = LETTER_FONT.render(text.upper(), True, TEXT_COLOR)
    input_rect = input_render.get_rect(center=input_rect.center)
    screen.blit(input_render, input_rect)


def draw_submit_button(screen, results):
    button_rect = pygame.Rect(0, 0, 70, 30)
    button_rect.topleft = (4 * (CELL_SIZE + MARGIN) + 10, (len(results) + 1) * (CELL_SIZE + MARGIN) + 10)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, 1)

    button_text = LETTER_FONT.render("Submit", True, TEXT_COLOR)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    return button_rect

def draw_message(screen, msg):
    msg_rect = pygame.Rect(0, WINDOW_HEIGHT - MSG_BOX_HEIGHT, WINDOW_WIDTH, MSG_BOX_HEIGHT)
    pygame.draw.rect(screen, INPUT_COLOR, msg_rect)
    pygame.draw.rect(screen, (0, 0, 0), msg_rect, 1)

    msg_render = RESULT_FONT.render(msg, True, TEXT_COLOR)
    msg_rect = msg_render.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - MSG_BOX_HEIGHT // 2))
    screen.blit(msg_render, msg_rect)

def main():
    words_list = ["tree", "yard", "door", "book", "rain", "wind", "bell",
    "ship", "fish", "lock"]
    word = choose_word(words_list)

    pygame.display.set_caption('4-Letter Wordle Game')
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    attempts = 6
    guesses = []
    results = []
    current_text = ""

    while attempts > 0:
        screen.fill(BG_COLOR)
        draw_grid(screen, guesses, results)
        custom_text_input(screen, current_text)
        submit_button_rect = draw_submit_button(screen, results)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN and len(current_text) == 4:
                    guess = current_text.lower()
                    guesses.append(guess)
                    correct_position, correct_letters = compare_words(word, guess)
                    results.append((correct_position, correct_letters))

                    if len(correct_position) == 4:
                        break

                    attempts -= 1
                    current_text = ""

                elif event.key == K_BACKSPACE:
                    current_text = current_text[:-1]
                else:
                    if len(current_text) < 4:
                        current_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if submit_button_rect.collidepoint(mouse_x, mouse_y) and len(current_text) == 4:
                    guess = current_text.lower()
                    guesses.append(guess)
                    correct_position, correct_letters = compare_words(word, guess)
                    results.append((correct_position, correct_letters))

                    if len(correct_position) == 4:
                        break

                    attempts -= 1
                    current_text = ""

        pygame.display.flip()
        pygame.time.delay(100)






    end_message = ""
    if attempts == 0:
        end_message = f"Sorry, you ran out of attempts. The word was '{word}'."
    else:
        end_message = f"Congratulations! You guessed the word '{word}' correctly!"

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            draw_message(screen, end_message)
            pygame.display.flip()
            pygame.time.delay(100)

if __name__ == "__main__":
    main()

