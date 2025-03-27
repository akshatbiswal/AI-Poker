from agents.agent import Agent
from gym_env import PokerEnv
import random
from treys import Evaluator
action_types = PokerEnv.ActionType
action_types = PokerEnv.ActionType
int_to_card = PokerEnv.int_to_card

class PlayerAgent(Agent):
    def __name__(self):
        return "PlayerAgent"
    
    def __init__(self, stream: bool = False):
        super().__init__(stream)
        self.evaluator = Evaluator()

    def act(self, observation, reward, terminated, truncated, info):
        # Log new street starts with important info
        if observation["street"] == 0:  # Preflop
            self.logger.debug(f"Hole cards: {[int_to_card(c) for c in observation['my_cards']]}")
        elif observation["community_cards"]:  # New community cards revealed
            visible_cards = [c for c in observation["community_cards"] if c != -1]
            if visible_cards:
                street_names = ["Preflop", "Flop", "Turn", "River"]
                self.logger.debug(f"{street_names[observation['street']]}: {[int_to_card(c) for c in visible_cards]}")

        my_cards = [int(card) for card in observation["my_cards"]]
        community_cards = [card for card in observation["community_cards"] if card != -1]
        opp_discarded_card = [observation["opp_discarded_card"]] if observation["opp_discarded_card"] != -1 else []
        opp_drawn_card = [observation["opp_drawn_card"]] if observation["opp_drawn_card"] != -1 else []

        # Calculate equity through Monte Carlo simulation
        shown_cards = my_cards + community_cards + opp_discarded_card + opp_drawn_card
        non_shown_cards = [i for i in range(27) if i not in shown_cards]

        def evaluate_hand(cards):
            my_cards, opp_cards, community_cards = cards
            my_cards = list(map(int_to_card, my_cards))
            opp_cards = list(map(int_to_card, opp_cards))
            community_cards = list(map(int_to_card, community_cards))
            my_hand_rank = self.evaluator.evaluate(my_cards, community_cards)
            opp_hand_rank = self.evaluator.evaluate(opp_cards, community_cards)
            return my_hand_rank < opp_hand_rank

        # Run Monte Carlo simulation
        num_simulations = 1000
        wins = sum(
            evaluate_hand((my_cards, opp_drawn_card + drawn_cards[: 2 - len(opp_drawn_card)], community_cards + drawn_cards[2 - len(opp_drawn_card) :]))
            for _ in range(num_simulations)
            if (drawn_cards := random.sample(non_shown_cards, 7 - len(community_cards) - len(opp_drawn_card)))
        )
        equity = wins / num_simulations

        # Calculate pot odds
        continue_cost = observation["opp_bet"] - observation["my_bet"]
        pot_size = observation["my_bet"] + observation["opp_bet"]
        pot_odds = continue_cost / (continue_cost + pot_size) if continue_cost > 0 else 0

        self.logger.debug(f"Equity: {equity:.2f}, Pot odds: {pot_odds:.2f}")

        # Decision making
        raise_amount = 0
        card_to_discard = -1

        # Only log very significant decisions at INFO level
        if equity > 0.8 and observation["valid_actions"][action_types.RAISE.value]:
            raise_amount = min(int(pot_size * 0.75), observation["max_raise"])
            raise_amount = max(raise_amount, observation["min_raise"])
            action_type = action_types.RAISE.value
            if raise_amount > 20:  # Only log large raises
                self.logger.info(f"Large raise to {raise_amount} with equity {equity:.2f}")
        elif equity >= pot_odds and observation["valid_actions"][action_types.CALL.value]:
            action_type = action_types.CALL.value
        elif observation["valid_actions"][action_types.CHECK.value]:
            action_type = action_types.CHECK.value
        elif observation["valid_actions"][action_types.DISCARD.value]:
            action_type = action_types.DISCARD.value
            card_to_discard = random.randint(0, 1)
            self.logger.debug(f"Discarding card {card_to_discard}: {int_to_card(my_cards[card_to_discard])}")
        else:
            action_type = action_types.FOLD.value
            if observation["opp_bet"] > 20:  # Only log significant folds
                self.logger.info(f"Folding to large bet of {observation['opp_bet']}")

        return action_type, raise_amount, card_to_discard

    def observe(self, observation, reward, terminated, truncated, info):
        if terminated and abs(reward) > 20:  # Only log significant hand results
            self.logger.info(f"Significant hand completed with reward: {reward}")


    # def __init__(self, stream: bool = True):
    #     super().__init__(stream)
    #     # Initialize any instance variables here
    #     self.hand_number = 0
    #     self.last_action = None
    #     self.won_hands = 0
    #     self.evaluator = Evaluator()
    #     self.hand_strength_cache = {}  # For memoization

    # def act(self, observation, reward, terminated, truncated, info):
    #     # Example of using the logger
    #     if observation["street"] == 0 and info["hand_number"] % 50 == 0:
    #         self.logger.info(f"Hand number: {info['hand_number']}")

    #     # First, get the list of valid actions we can take
    #     valid_actions = observation["valid_actions"]
        
    #     # Get indices of valid actions (where value is 1)
    #     valid_action_indices = [i for i, is_valid in enumerate(valid_actions) if is_valid]
        
    #     # Randomly choose one of the valid action indices
    #     action_type = random.choice(valid_action_indices)
        
    #     # Set up our response values
    #     raise_amount = 0
    #     card_to_discard = -1  # -1 means no discard
        
    #     # If we chose to raise, pick a random amount between min and max
    #     if action_type == action_types.RAISE.value:
    #         if observation["min_raise"] == observation["max_raise"]:
    #             raise_amount = observation["min_raise"]
    #         else:
    #             raise_amount = random.randint(
    #                 observation["min_raise"],
    #                 observation["max_raise"]
    #             )
        
    #     # If we chose to discard, randomly pick one of our two cards (0 or 1)
    #     if action_type == action_types.DISCARD.value:
    #         card_to_discard = random.randint(0, 1)
        
    #     return action_type, raise_amount, card_to_discard

    # def observe(self, observation, reward, terminated, truncated, info):
    #     # Log interesting events when observing opponent's actions
    #     pass
    #     if terminated:
    #         self.logger.info(f"Game ended with reward: {reward}")
    #         self.hand_number += 1
    #         if reward > 0:
    #             self.won_hands += 1
    #         self.last_action = None
    #     else:
    #         # log observation keys
    #         self.logger.info(f"Observation keys: {observation}")
 