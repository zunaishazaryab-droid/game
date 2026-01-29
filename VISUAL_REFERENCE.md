# 🎨 Forget to Win - Visual Mockups & Code Reference

This document contains all ASCII mockups and key code snippets for quick reference.

---

## 📱 MOCKUP 1: Title Screen

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     ███████╗ ██████╗ ██████╗  ██████╗ ███████╗████████╗            ║
║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝            ║
║     █████╗  ██║   ██║██████╔╝██║  ███╗█████╗     ██║               ║
║     ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝     ██║               ║
║     ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗   ██║               ║
║     ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝               ║
║                                                                      ║
║                    ████████╗ ██████╗                                ║
║                    ╚══██╔══╝██╔═══██╗                               ║
║                       ██║   ██║   ██║                               ║
║                       ██║   ██║   ██║                               ║
║                       ██║   ╚██████╔╝                               ║
║                       ╚═╝    ╚═════╝                                ║
║                                                                      ║
║     ██╗    ██╗██╗███╗   ██╗                                         ║
║     ██║    ██║██║████╗  ██║                                         ║
║     ██║ █╗ ██║██║██╔██╗ ██║                                         ║
║     ██║███╗██║██║██║╚██╗██║                                         ║
║     ╚███╔███╔╝██║██║ ╚████║                                         ║
║      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝                                         ║
║                                                                      ║
║              🧠 Master the Art of Selective Forgetting 🧠            ║
║                                                                      ║
║                    Press ENTER to Begin...                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Implementation**: `game_engine.py` → `GameDisplay.show_title_screen()`

---

## 📱 MOCKUP 2: Memorization Phase

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🧠 FORGET TO WIN                          Level: 3/5  Score: 245  ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                    ┃
┃  📋 MEMORIZATION PHASE                                             ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                    ┃
┃  ⏱️  Time Remaining: 8s                                            ┃
┃  [████████████████████░░░░░░░░] 70%                               ┃
┃                                                                    ┃
┃  ┌────────────────────────────────────────────────────────────┐   ┃
┃  │                                                            │   ┃
┃  │   ✅  Water          ❌  Soda           ✅  Exercise       │   ┃
┃  │                                                            │   ┃
┃  │   ❌  Junk Food      ✅  Salad          ❌  Stress         │   ┃
┃  │                                                            │   ┃
┃  │   ✅  Sleep          ❌  Scrolling      ✅  Reading        │   ┃
┃  │                                                            │   ┃
┃  └────────────────────────────────────────────────────────────┘   ┃
┃                                                                    ┃
┃  💡 Remember the ✅ items. Forget the ❌ items!                    ┃
┃                                                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Implementation**: `main.py` → `ForgetToWinGame.memorization_phase()`

---

## 📱 MOCKUP 3: Recall Phase

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🧠 FORGET TO WIN                          Level: 3/5  Score: 245  ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                    ┃
┃  🎯 RECALL PHASE                                                   ┃
┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃
┃                                                                    ┃
┃  Which items were marked as GOOD (✅)?                             ┃
┃  Select all that apply (comma-separated numbers):                 ┃
┃                                                                    ┃
┃  ┌────────────────────────────────────────────────────────────┐   ┃
┃  │                                                            │   ┃
┃  │   1. Water          4. Junk Food       7. Sleep           │   ┃
┃  │   2. Soda           5. Salad           8. Scrolling        │   ┃
┃  │   3. Exercise       6. Stress          9. Reading          │   ┃
┃  │                                                            │   ┃
┃  └────────────────────────────────────────────────────────────┘   ┃
┃                                                                    ┃
┃  Your Answer: ▊                                                    ┃
┃                                                                    ┃
┃  💭 Remember: Only select the ✅ items you saw!                    ┃
┃                                                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Implementation**: `main.py` → `ForgetToWinGame.recall_phase()`

---

## 📱 MOCKUP 4: Level Results

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    🎉 LEVEL 3 COMPLETE! 🎉                          ║
║                                                                      ║
║  ┌────────────────────────────────────────────────────────────────┐ ║
║  │                      PERFORMANCE BREAKDOWN                     │ ║
║  ├────────────────────────────────────────────────────────────────┤ ║
║  │                                                                │ ║
║  │  ✅ Correctly Remembered:        4 / 5    (+40 pts)           │ ║
║  │  ❌ Incorrectly Remembered:      0 / 4    (+0 pts)            │ ║
║  │  😢 Forgotten Good Items:        1        (-5 pts)            │ ║
║  │  🎯 Accuracy:                    80%                           │ ║
║  │                                           ─────────            │ ║
║  │  💰 Level Score:                          +35 pts             │ ║
║  │  🔥 Streak Bonus (x2):                    +35 pts             │ ║
║  │                                           ═════════            │ ║
║  │  ⭐ TOTAL SCORE:                          315                 │ ║
║  │                                                                │ ║
║  └────────────────────────────────────────────────────────────────┘ ║
║                                                                      ║
║                      Current Rank: Focus Ninja 🥷                   ║
║                                                                      ║
║              [████████████████████░░░░░░] 81/100                    ║
║                   19 points to Zen Master!                          ║
║                                                                      ║
║                    Press ENTER for Level 4...                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Implementation**: `game_engine.py` → `LevelManager.display_level_result()`

---

## 📱 MOCKUP 5: Final Results

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                      🏆 GAME COMPLETE! 🏆                           ║
║                                                                      ║
║  ┌────────────────────────────────────────────────────────────────┐ ║
║  │                       FINAL STATISTICS                         │ ║
║  ├────────────────────────────────────────────────────────────────┤ ║
║  │                                                                │ ║
║  │  📊 Total Score:                     487 / 500                │ ║
║  │  🎯 Overall Accuracy:                92%                       │ ║
║  │  🔥 Best Streak:                     5 levels                  │ ║
║  │  ⏱️  Total Time:                     4m 32s                    │ ║
║  │                                                                │ ║
║  │  ┌──────────────────────────────────────────────────────────┐ │ ║
║  │  │                                                          │ │ ║
║  │  │              👑 ZEN MASTER 👑                            │ │ ║
║  │  │                                                          │ │ ║
║  │  │         "Mind like water, focus like laser"             │ │ ║
║  │  │                                                          │ │ ║
║  │  │              ⭐⭐⭐⭐⭐ (5/5)                            │ │ ║
║  │  │                                                          │ │ ║
║  │  └──────────────────────────────────────────────────────────┘ │ ║
║  │                                                                │ ║
║  └────────────────────────────────────────────────────────────────┘ ║
║                                                                      ║
║  💡 Daily Wisdom:                                                   ║
║  "Just like this game, your brain filters 99% of sensory input.     ║
║   Choose what to remember wisely."                                  ║
║                                                                      ║
║  ┌────────────────────────────────────────────────────────────────┐ ║
║  │  [P] Play Again    [H] High Scores    [Q] Quit                │ ║
║  └────────────────────────────────────────────────────────────────┘ ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Implementation**: `game_engine.py` → `LevelManager.display_final_results()`

---

## 💻 KEY CODE SNIPPETS

### 1. Scoring Algorithm

```python
@staticmethod
def calculate_level_score(
    correct_good: int,
    total_good: int,
    remembered_bad: int,
    streak: int
) -> Tuple[int, int, int]:
    """
    Calculate score for a level
    
    Returns:
        (base_score, streak_bonus, total_score)
    """
    forgotten_good = total_good - correct_good
    
    # Base score calculation
    base_score = (
        correct_good * GameConfig.POINTS_PER_CORRECT_GOOD -
        forgotten_good * GameConfig.PENALTY_PER_FORGOTTEN_GOOD -
        remembered_bad * GameConfig.PENALTY_PER_REMEMBERED_BAD
    )
    
    # Ensure base score doesn't go negative
    base_score = max(0, base_score)
    
    # Streak bonus
    streak_bonus = int(base_score * (streak * GameConfig.STREAK_MULTIPLIER))
    
    total_score = base_score + streak_bonus
    
    return base_score, streak_bonus, total_score
```

**File**: `game_engine.py` → `ScoreCalculator.calculate_level_score()`

---

### 2. Level Configuration

```python
LEVELS = {
    1: {"good_items": 3, "bad_items": 2, "display_time": 10, "distractors": []},
    2: {"good_items": 4, "bad_items": 3, "display_time": 8, "distractors": []},
    3: {"good_items": 5, "bad_items": 4, "display_time": 7, "distractors": []},
    4: {"good_items": 6, "bad_items": 5, "display_time": 6, "distractors": ["visual_camouflage"]},
    5: {"good_items": 7, "bad_items": 6, "display_time": 5, "distractors": ["visual_camouflage", "temporal_interference"]},
}
```

**File**: `game_engine.py` → `GameConfig.LEVELS`

---

### 3. Rank System

```python
RANKS = [
    (0, 20, "Information Overloaded", "🤯", "Your brain needs a reboot"),
    (21, 40, "Digital Hoarder", "📦", "Still holding onto junk data"),
    (41, 60, "Selective Learner", "🎓", "Getting the hang of it"),
    (61, 80, "Focus Ninja", "🥷", "Distractions fear you"),
    (81, 95, "Zen Master", "🧘", "Mind like water"),
    (96, 100, "Cognitive Elite", "👑", "You've achieved mental clarity"),
]
```

**File**: `game_engine.py` → `GameConfig.RANKS`

---

### 4. Item Pool Example

```python
ITEM_THEMES = {
    "healthy_habits": {
        "good": ["Water", "Exercise", "Sleep", "Salad", "Meditation"],
        "bad": ["Soda", "Junk Food", "Stress", "Scrolling", "All-nighter"]
    },
    "code_quality": {
        "good": ["def function()", "try-except", "git commit", "Code Review", "Unit Test"],
        "bad": ["funtion()", "bare except:", "git push --force", "Skip Review", "No Tests"]
    },
    # ... 6 more themes
}
```

**File**: `item_pool.py` → `ItemPool.ITEM_THEMES`

---

### 5. Rich Progress Bar

```python
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    console=console,
    transient=True
) as progress:
    task = progress.add_task("[cyan]Memorizing...", total=display_time)
    
    for i in range(display_time):
        time.sleep(1)
        progress.update(task, advance=1, description=f"[cyan]Time remaining: {display_time - i - 1}s")
```

**File**: `main.py` → `ForgetToWinGame.memorization_phase()`

---

### 6. Grid Display Formatting

```python
@staticmethod
def format_grid(items: List[Item], columns: int = 3) -> str:
    """Format items in a grid layout"""
    rows = []
    for i in range(0, len(items), columns):
        row_items = items[i:i + columns]
        row = "   ".join(str(item).ljust(20) for item in row_items)
        rows.append(f"  │   {row:<60}│")
    
    return "\n".join(rows)
```

**File**: `item_pool.py` → `ItemDisplay.format_grid()`

---

## 🎯 SCORING EXAMPLES

| Scenario | Correct | Forgot | Wrong | Base | Bonus | Total | Accuracy |
|----------|---------|--------|-------|------|-------|-------|----------|
| Perfect Score | 5 | 0 | 0 | +50 | +30 | 80 | 100% |
| Good Performance | 4 | 1 | 1 | +35 | +14 | 49 | 77.8% |
| Average | 3 | 2 | 2 | +20 | +0 | 20 | 55.6% |
| Poor | 2 | 3 | 3 | +5 | +0 | 5 | 33.3% |

**Formula**:
```
base_score = (correct × 10) - (forgot × 5) - (wrong × 3)
streak_bonus = base_score × (streak × 0.2)
total_score = base_score + streak_bonus
accuracy = (correct + (total_bad - wrong)) / total_items × 100
```

---

## 🎨 COLOR SCHEME (Rich Library)

| Element | Color | Rich Code |
|---------|-------|-----------|
| Headers | Cyan | `[cyan]` or `style="cyan"` |
| Good Items | Green | `[green]` or `style="green"` |
| Bad Items | Red | `[red]` or `style="red"` |
| Scores | Yellow | `[yellow]` or `style="yellow"` |
| Warnings | Yellow | `[yellow]` |
| Success | Green | `[green]` |
| Emphasis | Bold Cyan | `[bold cyan]` |
| Dim Text | Dim | `[dim]` |

---

## 📊 GAME FLOW DIAGRAM

```
┌─────────────────┐
│  Title Screen   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Level 1-5      │◄──────┐
│  ┌───────────┐  │       │
│  │Memorize   │  │       │
│  └─────┬─────┘  │       │
│        │        │       │
│  ┌─────▼─────┐  │       │
│  │  Recall   │  │       │
│  └─────┬─────┘  │       │
│        │        │       │
│  ┌─────▼─────┐  │       │
│  │  Results  │  │       │
│  └─────┬─────┘  │       │
└────────┼────────┘       │
         │                │
         ├─ Next Level ───┘
         │
         ▼
┌─────────────────┐
│ Final Results   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Menu           │
│  [P]lay Again   │
│  [H]igh Scores  │
│  [Q]uit         │
└─────────────────┘
```

---

## 🚀 QUICK START COMMANDS

```bash
# Install dependencies
pip install rich

# Run full game
python main.py

# Run demo (view all components)
python demo.py

# Windows quick start
start.bat
```

---

## 📝 FILE STRUCTURE

```
forgetwingame/
├── main.py              # Main game loop
├── game_engine.py       # Scoring, level management, UI
├── item_pool.py         # Item themes and display
├── demo.py              # Component showcase
├── requirements.txt     # Dependencies
├── start.bat            # Windows launcher
├── README.md           # Full documentation
└── VISUAL_REFERENCE.md # This file
```

---

**Created with 🧠 and ✨ for premium terminal gaming experience!**
