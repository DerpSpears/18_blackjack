from cards import Deck, hand_value, hand_text, card_name, is_blackjack, is_soft

STARTING_CHIPS = 100
BLACKJACK_PAYOUT = 1.5
DEALER_STANDS_ON = 17


class Blackjack:
    def __init__(self, chips=STARTING_CHIPS):
        self.chips = chips

    # ---------- display ----------

    def show(self, player, dealer, hide=True):
        if hide:
            print("Dealer:", card_name(dealer[0]), "??")
        else:
            print("Dealer:", hand_text(dealer), "=", hand_value(dealer))
        soft = " (soft)" if is_soft(player) else ""
        print("Player:", hand_text(player), "=", hand_value(player), end="")
        print(soft)

    # ---------- input ----------

    def ask_wager(self):
        """Return a valid wager, or None if the player quits.

        An invalid wager is rejected and re-asked; the bankroll is untouched.
        """
        while True:
            raw = input(f"Wager (1-{self.chips}, [q] to quit): ").strip().lower()
            if raw == "q":
                return None
            if not raw.isdigit():
                print("Invalid wager: enter a whole number of chips.")
                continue
            wager = int(raw)
            if wager < 1:
                print("Invalid wager: must be at least 1 chip.")
            elif wager > self.chips:
                print(f"Invalid wager: you only have {self.chips} chips.")
            else:
                return wager

    # ---------- settlement ----------

    def settle(self, result, wager):
        """Apply the result to the bankroll exactly once."""
        if result == "blackjack":
            won = int(wager * BLACKJACK_PAYOUT)
            self.chips += won
            print(f"Blackjack! You win {won} chips.")
        elif result == "win":
            self.chips += wager
            print(f"Player wins {wager} chips.")
        elif result == "lose":
            self.chips -= wager
            print(f"Dealer wins. You lose {wager} chips.")
        else:
            print("Push. Your wager is returned.")
        print("Chips:", self.chips)

    # ---------- one round ----------

    def round(self):
        """Play one round. Returns False when the player quits."""
        wager = self.ask_wager()
        if wager is None:
            return False

        deck = Deck()
        player = [deck.draw(), deck.draw()]
        dealer = [deck.draw(), deck.draw()]
        print(f"\nYou bet {wager} chips.")
        self.show(player, dealer)

        # Naturals are resolved before any player action.
        if is_blackjack(player) or is_blackjack(dealer):
            self.show(player, dealer, hide=False)
            if is_blackjack(player) and is_blackjack(dealer):
                self.settle("push", wager)
            elif is_blackjack(player):
                self.settle("blackjack", wager)
            else:
                print("Dealer has blackjack.")
                self.settle("lose", wager)
            return True

        round_over = False
        while not round_over:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()
            if key == "q":
                print("Round abandoned; your wager is returned.")
                return False
            if key == "s":
                print("You stand on", hand_value(player), end=".\n")
                break
            if key != "h":
                print("Unknown command. Use h, s or q.")
                continue

            card = deck.draw()
            if card is None:
                print("Deck is empty; round cancelled and wager returned.")
                return True
            player.append(card)
            print("You draw", card_name(card), end=".\n")
            self.show(player, dealer)
            if hand_value(player) > 21:
                print("Bust.")
                self.settle("lose", wager)
                round_over = True

        if round_over:
            return True

        print("Dealer reveals", card_name(dealer[1]), end=".\n")
        while hand_value(dealer) < DEALER_STANDS_ON:
            card = deck.draw()
            if card is None:
                print("Deck is empty; round cancelled and wager returned.")
                return True
            dealer.append(card)
            print("Dealer draws", card_name(card), end=".\n")
        self.show(player, dealer, hide=False)

        pv, dv = hand_value(player), hand_value(dealer)
        if dv > 21:
            print("Dealer busts.")
            self.settle("win", wager)
        elif pv > dv:
            self.settle("win", wager)
        elif pv < dv:
            self.settle("lose", wager)
        else:
            self.settle("push", wager)
        return True

    # ---------- session ----------

    def run(self):
        print("Blackjack - starting chips:", self.chips)
        while self.chips > 0:
            if not self.round():
                break
            if input("\nPlay again? [y/n]: ").strip().lower() != "y":
                break
            print()
        if self.chips <= 0:
            print("Out of chips.")
        print("You leave the table with", self.chips, end=" chips.\n")
