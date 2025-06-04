# Word Guesser Game 🎯

A fun and interactive word guessing game built with Python and Tkinter. Test your vocabulary skills by guessing words from different categories with varying difficulty levels!

![Word Guesser Game](title.png)

## 📖 Description

Word Guesser is a classic hangman-style game where players try to guess a hidden word by suggesting letters. The game features multiple word categories, difficulty levels, and an engaging graphical interface with sound effects and background music.

## ✨ Features

### 🎮 Game Modes
- **Multiple Categories**: Choose from Countries, Foods, Vocabulary, or All categories
- **Difficulty Levels**: 
  - Easy (15 strikes)
  - Medium (10 strikes) 
  - Hard (5 strikes)
- **Word Length Options**:
  - Short (5 letters)
  - Normal (10 letters)
  - Long (15 letters)

### 🎨 User Experience
- **Intuitive GUI**: Clean, paper-themed interface built with Tkinter
- **Sound Effects**: Background music and typewriter sound effects
- **Interactive Elements**: Hover effects, confirmation dialogs, and smooth transitions
- **Scoreboard**: Track your best performances and word completion stats
- **Whole Word Guessing**: Option to guess the entire word at once (high risk, high reward!)

### 📊 Game Features
- **Real-time Feedback**: See guessed letters and remaining strikes
- **Progress Tracking**: Visual representation of word completion
- **Player Profiles**: Enter your name and track individual performance
- **Game Rules**: Built-in rules and instructions page
- **Restart Functionality**: Easy game restart without closing the application

## 🛠️ Installation

### Prerequisites
- Python 3.x
- Tkinter (usually comes with Python)
- Windows OS (for `winsound` module compatibility)

### Setup
1. **Clone or download the repository**:
   ```bash
   git clone https://github.com/yourusername/word-guesser.git
   cd word-guesser
   ```

2. **Ensure all files are in the same directory**:
   - `main.py` (main game file)
   - Word bank files: `bank_countries.txt`, `bank_foods.txt`, `bank_vocabs.txt`
   - Image assets: `*.png` files for UI elements
   - Sound files: `music.wav`, `typewriter_sound.wav`
   - Icon files: `*.ico` files

3. **Run the game**:
   ```bash
   python main.py
   ```

## 🎯 How to Play

### Getting Started
1. **Launch the game** by running `main.py`
2. **Enter your name** when prompted
3. **Read the rules** (optional but recommended for first-time players)
4. **Configure your game**:
   - Select difficulty level (Easy/Medium/Hard)
   - Choose word category (Country/Food/Vocabulary/All)
   - Set word length preference (Short/Normal/Long)

### Gameplay
1. **Start guessing**: Use your keyboard to guess letters
2. **Track progress**: 
   - Correct letters appear in their positions
   - Incorrect letters are displayed below
   - Strike counter shows remaining attempts
3. **Win conditions**:
   - Guess all letters correctly
   - Successfully guess the entire word using the "Know the word already?" feature
4. **Lose condition**: Exceed the strike limit for your chosen difficulty

### Game Controls
- **Keyboard**: Type letters to make guesses
- **Back Button**: Return to previous screen (with confirmation)
- **End Button**: Exit the game entirely
- **Restart**: Use File menu to restart the game
- **Whole Word Guess**: Click the yellow button during gameplay

## 📁 Project Structure

```
Word Guesser/
├── main.py                 # Main game application
├── scoreboard.txt          # Player score tracking
├── bank_countries.txt      # Country names word bank (192 words)
├── bank_foods.txt          # Food items word bank (128 words)
├── bank_vocabs.txt         # Vocabulary word bank (4319 words)
├── music.wav              # Background music
├── typewriter_sound.wav   # Typing sound effects
├── title.png              # Main title image
├── title_small.png        # Small title for game screen
├── rules_page.png         # Rules display image
├── won.png                # Victory screen image
├── lost.png               # Game over screen image
├── start_btn.png          # Start button graphics
├── start_btn2.png         # Alternative start button
├── rules_btn.png          # Rules button graphics
├── bknd.png               # Paper background texture
├── country.png            # Country category icon
├── food.png               # Food category icon
├── vocab.png              # Vocabulary category icon
├── all.png                # All categories icon
├── guess.ico              # Popup window icon
└── icon.ico               # Main application icon
```

## 🏆 Scoring System

The game tracks your performance in the `scoreboard.txt` file with the following format:
```
[Player Name] [Guesses Made] [Difficulty] (Word: [The Word])
```

**Example entries**:
- `john 12 Medium (Word: elephant)`
- `sarah 8 Hard (Word: pizza)`

## 🎨 Customization

### Adding New Words
You can expand the word banks by editing the text files:
- **Countries**: Add to `bank_countries.txt`
- **Foods**: Add to `bank_foods.txt`
- **Vocabulary**: Add to `bank_vocabs.txt`

Format: One word per line, case-insensitive

### Modifying Difficulty
In `main.py`, you can adjust strike limits:
```python
easy_strike_limit = 15    # Easy difficulty
medium_strike_limit = 10  # Medium difficulty  
hard_strike_limit = 5     # Hard difficulty
```

### Changing Word Length Filters
Modify the word length categories:
```python
short = 5      # Maximum letters for "short" words
normal = 10    # Maximum letters for "normal" words
long = 15      # Maximum letters for "long" words
```

## 🔧 Technical Details

### Built With
- **Python 3.x**: Core programming language
- **Tkinter**: GUI framework for the user interface
- **winsound**: Windows sound API for audio features
- **PIL/Pillow**: Image processing (if using advanced image features)

### Key Components
- **Canvas-based UI**: All screens use Tkinter Canvas for flexible layout
- **Event-driven Architecture**: Keyboard and mouse event handling
- **State Management**: Global variables track game state across screens
- **File I/O**: Reading word banks and writing scoreboard data

## 🐛 Troubleshooting

### Common Issues

**Game won't start**:
- Ensure all image and sound files are in the same directory as `main.py`
- Check that Python has Tkinter support
- Verify Python version compatibility (3.x required)

**No sound**:
- `winsound` module only works on Windows
- For other operating systems, you may need to replace sound functionality

**Missing images**:
- Ensure all `.png` and `.ico` files are present
- Check file permissions and paths

**Word banks empty**:
- Verify `.txt` files contain word lists
- Check file encoding (should be UTF-8)

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Future Enhancements

- [ ] **Cross-platform audio**: Replace `winsound` with a cross-platform solution
- [ ] **Multiplayer mode**: Add network play for multiple players
- [ ] **Themes**: Additional visual themes and color schemes
- [ ] **Hints system**: Optional letter hints for difficult words
- [ ] **Statistics**: More detailed player statistics and analytics
- [ ] **Word definitions**: Display word meanings after completion
- [ ] **Mobile version**: Touch-friendly mobile interface
- [ ] **Online leaderboards**: Global player rankings

## 🙏 Acknowledgments

- Word banks compiled from various educational and reference sources
- UI design inspired by classic paper-and-pencil games
- Sound effects and music enhance the nostalgic gaming experience

---