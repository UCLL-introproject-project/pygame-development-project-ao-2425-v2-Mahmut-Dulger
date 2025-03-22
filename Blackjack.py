# black jack in python wth pygame!
import copy
import random
import pygame

pygame.init()
# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False
# win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
hand_1 = []  # First split hand
hand_2 = []  # Second split hand
active_hand = 0  # 0 = normal hand, 1 = first split hand, 2 = second split hand
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...', '2 Wins!', '2 Losses!', '1 Win, 1 Loss!']
split_hand = False
# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck


# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))


# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    if active_hand == 0:  # Normal hand
        for i in range(len(player)):
            pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
            screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + (5 * i)))
            pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
    elif active_hand == 1:  # First split hand
        for i in range(len(hand_1)):
            pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
            screen.blit(font.render(hand_1[i], True, 'black'), (75 + 70 * i, 465 + (5 * i)))
            pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
    elif active_hand == 2:  # Second split hand
        for i in range(len(hand_2)):
            pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
            screen.blit(font.render(hand_2[i], True, 'black'), (75 + 70 * i, 465 + (5 * i)))
            pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    # Draw dealer cards
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score


# draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []
    # initially on startup (not active) only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    # once game started, shot hit and stand buttons and win/loss records
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 840))
        # If splitting is possible, show the split button
        if split_hand and len(my_hand) == 2:
            split_btn = pygame.draw.rect(screen, 'white', [150, 600, 300, 100], 0, 5)
            pygame.draw.rect(screen, 'green', [150, 600, 300, 100], 3, 5)
            split_text = font.render('SPLIT', True, 'black')
            screen.blit(split_text, (230, 630))
            button_list.append(split_btn)
    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list


# Update check_endgame to ensure add_score is used correctly
# Update the check_endgame function to fix score tracking and ensure no score increment until the next hand
def check_endgame(hand_act, deal_score, player_score, result, totals, add):
    # Check if the dealer's score is finalized (>= 17) and if the player's turn is over
    if not hand_act and deal_score >= 17:
        # Normal hand case (no split)
        if active_hand == 0:
            if player_score > 21:
                result = 1  # Player busts
            elif deal_score < player_score <= 21 or deal_score > 21:
                result = 2  # Player wins
            elif player_score < deal_score <= 21:
                result = 3  # Dealer wins
            else:
                result = 4  # Draw

        # Split hand case (after both hands are played)
        elif active_hand == 2:  # After both split hands are played
            hand_1_score = calculate_score(hand_1)
            hand_2_score = calculate_score(hand_2)

            # Initialize results for each hand
            hand_1_result = 0  # 0 = undecided, 1 = loss, 2 = win, 3 = draw
            hand_2_result = 0  # Same for hand 2

            # Evaluate first split hand
            if hand_1_score > 21:
                hand_1_result = 1  # Loss
            elif deal_score < hand_1_score <= 21 or deal_score > 21:
                hand_1_result = 2  # Win
            elif hand_1_score < deal_score <= 21:
                hand_1_result = 1  # Loss
            else:
                hand_1_result = 3  # Draw

            # Evaluate second split hand
            if hand_2_score > 21:
                hand_2_result = 1  # Loss
            elif deal_score < hand_2_score <= 21 or deal_score > 21:
                hand_2_result = 2  # Win
            elif hand_2_score < deal_score <= 21:
                hand_2_result = 1  # Loss
            else:
                hand_2_result = 3  # Draw

            # Determine overall result for split hands
            if hand_1_result == 2 and hand_2_result == 2:
                result = 5  # Two wins (both split hands win)
            elif hand_1_result == 1 and hand_2_result == 1:
                result = 6  # Two losses (both split hands lose)
            else:
                result = 7  # Mixed result (1 win, 1 loss)



        # Update totals only once after the round is finished
        if add:
            if result in [1, 3, 6]:  # Player loses
                totals[1] += 1
            elif result in [2, 5]:  # Player wins
                totals[0] += 1
            elif result in [4, 7]:  # Draw
                totals[2] += 1
            add = False  # Prevent further updates until next hand

    return result, totals, add

# main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')
    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        # Check if the player can split
        if my_hand[0] == my_hand[1]:
            split_hand = True  # Enable the option to split
        initial_deal = False
    # once game is activated, and dealt, calculate scores and display cards
    if active:
        if active_hand == 0:  # Normal hand
            player_score = calculate_score(my_hand)
        elif active_hand == 1:  # First split hand
            player_score = calculate_score(hand_1)
        elif active_hand == 2:  # Second split hand
            player_score = calculate_score(hand_2)

        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome)

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    hand_1 = []  # Reset first split hand
                    hand_2 = []  # Reset second split hand
                    active_hand = 0  # Reset to normal hand
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    split_hand = False  # Reset split option
                    add_score = True  # Reset add_score flag
                    player_score = 0  # Reset player score
                    dealer_score = 0  # Reset dealer score
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and hand_active:
                    if active_hand == 0:  # Normal hand
                        my_hand, game_deck = deal_cards(my_hand, game_deck)
                        player_score = calculate_score(my_hand)
                    elif active_hand == 1:  # First split hand
                        hand_1, game_deck = deal_cards(hand_1, game_deck)
                        if calculate_score(hand_1) >= 21:
                            active_hand = 2  # Move to second hand if first busts or hits 21
                    elif active_hand == 2:  # Second split hand
                        hand_2, game_deck = deal_cards(hand_2, game_deck)
                        if calculate_score(hand_2) >= 21:
                            hand_active = False  # Both hands are done
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos):
                    if active_hand == 1:  # If standing on first hand, move to second hand
                        active_hand = 2
                    elif active_hand == 2:  # If standing on second hand, finish the turn
                        hand_active = False
                        reveal_dealer = True
                    else:  # If it's a normal (non-split) hand
                        hand_active = False
                        reveal_dealer = True
                # Handle splitting when "SPLIT" is clicked
                elif split_hand and len(buttons) > 2 and buttons[2].collidepoint(event.pos):
                    # Create two separate hands
                    hand_1 = [my_hand[0]]
                    hand_2 = [my_hand[1]]
                    my_hand = []  # Clear original hand

                    # Deal one additional card to each new hand
                    hand_1, game_deck = deal_cards(hand_1, game_deck)
                    hand_2, game_deck = deal_cards(hand_2, game_deck)

                    # Start playing the first hand
                    active_hand = 1
                    split_hand = False  # Disable split option after use
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        hand_1 = []  # Reset first split hand
                        hand_2 = []  # Reset second split hand
                        active_hand = 0  # Reset to normal hand
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        split_hand = False  # Reset split option
                        add_score = True  # Reset add_score flag
                        player_score = 0  # Reset player score
                        dealer_score = 0  # Reset dealer score


    # if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    # Automatically end turn for split hands if they bust or reach 21
    if active_hand == 1 and calculate_score(hand_1) >= 21:
        active_hand = 2  # Move to second hand
    elif active_hand == 2 and calculate_score(hand_2) >= 21:
        hand_active = False  # End turn if second hand is done

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()
pygame.quit()