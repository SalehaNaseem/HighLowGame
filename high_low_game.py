import streamlit as st
import random
from PIL import Image
import time
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="High-Low Game",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        font-size: 3rem !important;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        font-size: 1.5rem !important;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .round-header {
        font-size: 1.8rem !important;
        color: #0D47A1;
        margin-top: 1rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .number-display {
        font-size: 5rem !important;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    .result-correct {
        font-size: 1.5rem !important;
        color: #2E7D32;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        background-color: #E8F5E9;
        border-radius: 10px;
    }
    .result-incorrect {
        font-size: 1.5rem !important;
        color: #C62828;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        background-color: #FFEBEE;
        border-radius: 10px;
    }
    .score-display {
        font-size: 1.8rem !important;
        color: #424242;
        text-align: center;
        margin: 1.5rem 0;
    }
    .stButton > button {
        background-color: #1E88E5;
        color: white;
        font-size: 1.2rem;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        border: none;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #0D47A1;
        box-shadow: 1px 1px 6px rgba(0,0,0,0.3);
    }
    .choice-button {
        margin: 1rem 0;
    }
    .game-over {
        font-size: 2.5rem !important;
        color: #0D47A1;
        text-align: center;
        margin: 2rem 0;
        animation: pulsate 1.5s infinite alternate;
    }
    @keyframes pulsate {
        0% {
            transform: scale(1);
        }
        100% {
            transform: scale(1.05);
        }
    }
    .stats-container {
        background-color: #E3F2FD;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .history-table {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'round_number' not in st.session_state:
    st.session_state.round_number = 1
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'my_number' not in st.session_state:
    st.session_state.my_number = 0
if 'computer_number' not in st.session_state:
    st.session_state.computer_number = 0
if 'round_complete' not in st.session_state:
    st.session_state.round_complete = False
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'result' not in st.session_state:
    st.session_state.result = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

# Constants
NUM_ROUNDS = 5

# Game functions
def start_new_game():
    st.session_state.game_active = True
    st.session_state.round_number = 1
    st.session_state.score = 0
    st.session_state.my_number = random.randint(1, 100)
    st.session_state.computer_number = 0
    st.session_state.round_complete = False
    st.session_state.game_over = False
    st.session_state.result = None
    st.session_state.history = []

def next_round():
    if st.session_state.round_number < NUM_ROUNDS:
        st.session_state.round_number += 1
        st.session_state.my_number = random.randint(1, 100)
        st.session_state.computer_number = 0
        st.session_state.round_complete = False
        st.session_state.result = None
    else:
        st.session_state.game_over = True
        st.session_state.games_played += 1
        st.session_state.total_score += st.session_state.score
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score

def make_guess(guess):
    if not st.session_state.round_complete:
        st.session_state.computer_number = random.randint(1, 100)
        is_correct = False
        
        if guess == "higher":
            is_correct = st.session_state.my_number > st.session_state.computer_number
        else:  # guess == "lower"
            is_correct = st.session_state.my_number < st.session_state.computer_number
        
        if is_correct:
            st.session_state.score += 1
            st.session_state.result = "correct"
            # Trigger balloons for correct answer
            st.balloons()
        else:
            st.session_state.result = "incorrect"
            
        # Add to history
        st.session_state.history.append({
            "Round": st.session_state.round_number,
            "Your Number": st.session_state.my_number,
            "Computer Number": st.session_state.computer_number,
            "Your Guess": guess.capitalize(),
            "Result": "Correct" if is_correct else "Incorrect"
        })
        
        st.session_state.round_complete = True

# Sidebar
with st.sidebar:
    st.markdown("## Game Settings")
    st.markdown("---")
    
    # Game stats
    st.markdown("## Game Stats")
    st.markdown(f"**Games Played:** {st.session_state.games_played}")
    st.markdown(f"**Total Score:** {st.session_state.total_score}")
    st.markdown(f"**High Score:** {st.session_state.high_score}")
    
    # Rules
    st.markdown("---")
    st.markdown("## How to Play")
    st.markdown("""
    1. You'll be shown a random number between 1-100
    2. Guess if your number is higher or lower than the computer's number
    3. Score points for correct guesses
    4. Play 5 rounds per game
    5. Try to beat your high score!
    """)

# Main content
st.markdown('<h1 class="main-title">🎮 High-Low Game</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Test your luck! Guess if your number is higher or lower than the computer\'s.</p>', unsafe_allow_html=True)

# Start game button
if not st.session_state.game_active:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start New Game", key="start_game"):
            start_new_game()
else:
    # Game is active
    if not st.session_state.game_over:
        # Display current round
        st.markdown(f'<h2 class="round-header">Round {st.session_state.round_number} of {NUM_ROUNDS}</h2>', unsafe_allow_html=True)
        
        # Display player's number
        st.markdown('<p style="text-align: center; font-size: 1.5rem;">Your number is:</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="number-display">{st.session_state.my_number}</div>', unsafe_allow_html=True)
        
        # Buttons for higher or lower
        if not st.session_state.round_complete:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="choice-button">', unsafe_allow_html=True)
                higher_button = st.button("Higher", key=f"higher_{st.session_state.round_number}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="choice-button">', unsafe_allow_html=True)
                lower_button = st.button("Lower", key=f"lower_{st.session_state.round_number}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Handle button clicks
            if higher_button:
                make_guess("higher")
            elif lower_button:
                make_guess("lower")
        
        # Display result of the round
        if st.session_state.round_complete:
            # Show computer's number with animation
            st.markdown('<p style="text-align: center; font-size: 1.5rem;">Computer\'s number is:</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="number-display">{st.session_state.computer_number}</div>', unsafe_allow_html=True)
            
            if st.session_state.result == "correct":
                st.markdown(f'<div class="result-correct">Correct! 🎉</div>', unsafe_allow_html=True)
                # Also add confetti effect for perfect score
                if st.session_state.score == st.session_state.round_number and st.session_state.round_number == NUM_ROUNDS:
                    st.snow()
            else:
                st.markdown(f'<div class="result-incorrect">Incorrect! 😢</div>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="score-display">Your Score: {st.session_state.score}</div>', unsafe_allow_html=True)
            
            # Next round button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Next Round", key=f"next_round_{st.session_state.round_number}"):
                    next_round()
    
    # Game over
    if st.session_state.game_over:
        st.markdown('<div class="game-over">Game Over!</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-display">Final Score: {st.session_state.score} out of {NUM_ROUNDS}</div>', unsafe_allow_html=True)
        
        # Show a different message based on score
        if st.session_state.score == NUM_ROUNDS:
            st.markdown('<p style="text-align: center; font-size: 1.5rem;">Perfect score! You\'re a master of luck! 🏆</p>', unsafe_allow_html=True)
        elif st.session_state.score >= NUM_ROUNDS * 0.6:
            st.markdown('<p style="text-align: center; font-size: 1.5rem;">Great job! You have good intuition! 🌟</p>', unsafe_allow_html=True)
        elif st.session_state.score >= NUM_ROUNDS * 0.4:
            st.markdown('<p style="text-align: center; font-size: 1.5rem;">Not bad! Keep practicing! 👍</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="text-align: center; font-size: 1.5rem;">Better luck next time! 🍀</p>', unsafe_allow_html=True)
        
        # Play again button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Play Again", key="play_again"):
                start_new_game()
    
    # Game history
    if st.session_state.history:
        st.markdown("## Game History")
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        # Create a progress chart
        if len(st.session_state.history) > 1:
            st.markdown("### Performance Chart")
            cumulative_score = np.cumsum([1 if h["Result"] == "Correct" else 0 for h in st.session_state.history])
            rounds = list(range(1, len(st.session_state.history) + 1))
            chart_data = pd.DataFrame({
                "Round": rounds,
                "Cumulative Score": cumulative_score
            })
            st.line_chart(chart_data.set_index("Round"))