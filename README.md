# AI Poker Project

## Overview
This repository contains the implementation for Akshat and Neil's submission for Carnegie Mellon University's Data Science Club AI Poker Competition. We aimed to implement a modified Texas Hold'Em poker game where AI agents compete against each other.

## Modified Game Rules
- Uses a **27-card deck** (no face cards or clubs)
- Cards include 2-9 and Ace from diamonds (♦), hearts (♥), and spades (♠) suits only
- Each player may discard and redraw one card per hand before the turn card
- Discarded cards and drawn cards are revealed to opponents

### Hand Rankings (from strongest to weakest)
1. Straight Flush: Five consecutive cards of the same suit
2. Full House: Three of a kind plus a pair
3. Flush: Five cards of the same suit
4. Straight: Five consecutive cards of any suit
5. Three of a Kind: Three cards of the same rank
6. Two Pair: Two different pairs
7. One Pair: Two cards of the same rank
8. High Card: Highest single card

Special Ace Rule: The Ace can be used as either high (above 9) or low (below 2) when forming straights and straight flushes.

## Repository Structure

### Core Components
- `match.py`: Implements the poker match mechanics and game flow
- `gym_env.py`: Implements the OpenAI Gym environment for the poker game
- `player.py`: Base implementation of a player agent
- `run.py`: Main entry point for running matches between agents

### Agent Implementation
- `agents/`: Directory containing agent implementations
- `submission/`: Directory for tournament submissions
  - `RLplayer.py`: Reinforcement Learning based agent
  - `Probplayer.py`: Probability-based agent
  - `player.py`: Main player implementation

### Documentation
- `docs/rules.md`: Detailed tournament rules
- `docs/game-engine.md`: Technical details of the game engine
- `docs/terminology.md`: Poker terminology definitions
- `docs/submission.md`: Instructions for submitting agents

## Getting Started

### Installation
1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running a Match
To run a match between two agents:
```bash
python run.py
```

The configuration for the match is specified in `agent_config.json`.

### Training an RL Agent
To train a reinforcement learning agent:
```bash
python train_rl_agent.py
```

## Agent Development
To develop your own agent:
1. Create a new agent class that inherits from the `Agent` base class
2. Implement the required methods:
   - `__init__`: Initialize your agent
   - `act`: Determine the action based on the current observation
   - `observe`: Process rewards and information after actions

## Competition Format
- 1000 hands per match
- Stack resets between hands
- Total chips tracked across entire match
- Winner determined by having more chips at the end

## Authors
- Akshat Biswal
- Neil Raman

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 