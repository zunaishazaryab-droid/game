# Forget to Win 🧠

**Master the Art of Selective Forgetting**

A cognitive training game that challenges you to remember the important and forget the noise. Built with Python and Rich library for a beautiful terminal experience.

---

## 🎮 Game Overview

In a world drowning in information, **Forget to Win** teaches you the most valuable skill: **selective forgetting**. 

- **Remember** the good items (✅)
- **Forget** the bad items (❌)
- **Progress** through 5 challenging levels
- **Earn** ranks from "Information Overloaded" to "Cognitive Elite"

---

## ✨ Features

- 🎯 **5 Progressive Levels** - Increasing difficulty with less time and more items
- 🧠 **80 Thematic Items** - Across 8 categories (Health, Productivity, Code Quality, etc.)
- 🏆 **6 Rank Tiers** - Track your cognitive mastery
- 🔥 **Streak System** - Bonus points for consistent 80%+ accuracy
- 📊 **Detailed Statistics** - Performance breakdown after each level
- 💡 **Daily Wisdom** - Educational tips about memory and productivity
- 🎨 **Beautiful UI** - Rich terminal graphics with colors and animations

---

## 📋 Requirements

- **Python 3.8+**
- **Rich library** (for terminal UI)

---

## 🚀 Installation

### 1. Clone or Download

```bash
cd forgetwingame
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Game

```bash
python main.py
```

---

## 🎯 How to Play

### Game Flow

1. **Title Screen** - Press ENTER to start
2. **Memorization Phase** - Study items marked with [+] (good) and [-] (bad)
3. **Countdown Timer** - You have 5-10 seconds depending on level
4. **Recall Phase** - Select the numbers of GOOD items you remember
5. **Results** - See your performance, score, and rank
6. **Repeat** - Complete all 5 levels
7. **Final Results** - View overall statistics and rank

### Controls

- **ENTER** - Advance through screens
- **Type numbers** - Select items (e.g., `1,3,5`)
- **P** - Play again
- **H** - High scores (coming soon)
- **Q** - Quit

---

## 📊 Scoring System

### Points

- **+10 points** - Each correct good item remembered
- **-5 points** - Each good item forgotten
- **-3 points** - Each bad item incorrectly remembered

### Streak Bonus

- Maintain **80%+ accuracy** to build streak
- **+20% bonus** per streak level
- Example: 30 base points + 2x streak = 42 total points

### Ranks

| Score | Rank | Description |
|-------|------|-------------|
| 0-20 | Information Overloaded | Your brain needs a reboot |
| 21-40 | Digital Hoarder | Still holding onto junk data |
| 41-60 | Selective Learner | Getting the hang of it |
| 61-80 | Focus Ninja | Distractions fear you |
| 81-95 | Zen Master | Mind like water |
| 96-100 | Cognitive Elite | You've achieved mental clarity |

---

## 🎓 Item Categories

The game features **80 items** across **8 thematic categories**:

1. **Healthy Habits** - Water vs Soda, Exercise vs Junk Food
2. **Productivity** - Deep Work vs Procrastination, Focus vs Distraction
3. **Code Quality** - Unit Tests vs No Tests, Code Review vs Skip Review
4. **Cybersecurity** - HTTPS vs HTTP, 2FA vs Password123
5. **Financial Wisdom** - Save Money vs Impulse Buy, Budget vs Max Credit
6. **Critical Thinking** - Fact Check vs Trust me bro, Evidence vs Assume
7. **Emotional Intelligence** - Listen First vs Interrupt, Empathy vs Dismiss
8. **Learning** - Active Recall vs Passive Reading, Practice vs Copy Paste

---

## 🏗️ Project Structure

```
forgetwingame/
├── main.py              # Game controller and main loop
├── game_engine.py       # Game logic, scoring, state management
├── item_pool.py         # Item data and display formatting
├── requirements.txt     # Python dependencies
├── test_rich.py         # Rich library verification
├── README.md            # This file
└── docs/
    ├── prd/
    │   └── index.md     # Product Requirements Document
    ├── architecture/
    │   └── index.md     # System Architecture Document
    └── EPICS_STORIES.md # Development roadmap
```

---

## 🧪 Testing

### Test Rich Library

```bash
python test_rich.py
```

### Test Item Pool

```bash
python item_pool.py
```

### Test Game Engine

```bash
python game_engine.py
```

---

## 🎨 Design Patterns Used

- **Controller Pattern** - `ForgetToWinGame` orchestrates game flow
- **Singleton Pattern** - `GameConfig` for centralized configuration
- **Strategy Pattern** - `ScoreCalculator` for scoring algorithms
- **State Pattern** - `LevelManager` for state tracking
- **Repository Pattern** - `ItemPool` for data access
- **Data Transfer Object** - `LevelResult` for immutable data

---

## 📚 Documentation

Comprehensive documentation available in `docs/`:

- **PRD** (`docs/prd/index.md`) - Product requirements and user stories
- **Architecture** (`docs/architecture/index.md`) - System design and patterns
- **Epics & Stories** (`docs/EPICS_STORIES.md`) - Development breakdown

---

## 🚀 Roadmap (v1.1)

- [ ] High score persistence (save/load)
- [ ] Leaderboard system
- [ ] Difficulty settings (Easy/Normal/Hard)
- [ ] Custom item themes
- [ ] Sound effects
- [ ] Achievements system
- [ ] Timed mode (speedrun)

---

## 🤝 Contributing

This is a learning project! Feel free to:

- Report bugs
- Suggest features
- Improve documentation
- Add new item categories
- Enhance UI/UX

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🧠 Philosophy

> "The art of being wise is the art of knowing what to overlook."  
> — William James

**Forget to Win** is inspired by:

- **Cognitive Load Theory** - Your working memory is limited
- **Digital Minimalism** - Less is more
- **The Pareto Principle** - 80% of results from 20% of efforts
- **Selective Attention** - Focus on what matters

---

## 🎯 Tips for High Scores

1. **Focus on patterns** - Group items by category mentally
2. **Use chunking** - Remember 3-4 items at a time
3. **Visualize** - Create mental images
4. **Practice** - Your brain gets better with repetition
5. **Stay calm** - Stress hurts memory performance

---

## 💡 Daily Wisdom

The game includes 10 educational tips about memory, productivity, and cognitive science. Here are a few:

- "Your brain filters 99% of sensory input. Choose what to remember wisely."
- "Productivity isn't about doing more—it's about forgetting the unimportant."
- "Your brain's 'delete button' is sleep. 7-8 hours helps consolidate good memories."

---

## 👨‍💻 Development

**Version**: 1.0  
**Status**: ✅ Complete  
**Language**: Python 3.8+  
**UI Library**: Rich 13.0+  

**Development Stats**:
- **4 Epics** completed
- **14 User Stories** implemented
- **42 Story Points** delivered
- **~1,500 lines** of production code
- **~5,000 lines** of documentation

---

## 🙏 Acknowledgments

Built with:
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- Python - The language that makes everything possible
- Coffee - The fuel of developers ☕

---

**Ready to master selective forgetting? Run `python main.py` and start your journey!** 🚀🧠

---

*Remember: In a world of infinite information, the ability to forget is just as important as the ability to remember.*
"# game" 
