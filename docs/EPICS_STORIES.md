# Epics & User Stories
## Forget to Win - Development Roadmap

---

**Document Version**: 1.0  
**Last Updated**: January 29, 2026  
**Status**: ✅ Ready for Implementation  
**Owner**: Development Team  
**Related Documents**: PRD (`docs/prd/index.md`), Architecture (`docs/architecture/index.md`)

---

## 📋 Document Overview

This document breaks down the **Forget to Win** project into **4 Epics** with **14 User Stories** (Tasks). Each story is implementation-ready with:
- Clear acceptance criteria
- Technical implementation details
- Estimated effort (story points)
- Dependencies
- Testing requirements

---

## 🎯 Epic Summary

| Epic | Stories | Story Points | Priority | Status |
|------|---------|--------------|----------|--------|
| **Epic 1: Project Setup** | 3 | 8 | P0 | 🔵 Ready |
| **Epic 2: Core Game Engine** | 4 | 13 | P0 | 🔵 Ready |
| **Epic 3: Scoring & Evaluation** | 3 | 8 | P0 | 🔵 Ready |
| **Epic 4: UI/UX Implementation** | 4 | 13 | P1 | 🔵 Ready |
| **TOTAL** | **14** | **42** | - | 🔵 Ready |

---

## 📦 Epic 1: Project Setup

**Goal**: Establish project foundation, dependencies, and data layer

**Priority**: P0 (Critical)  
**Total Story Points**: 8  
**Dependencies**: None  
**Estimated Duration**: 1-2 days

---

### **Story 1.1: Project Initialization & Dependencies**

**As a** developer  
**I want to** set up the project structure and install dependencies  
**So that** I have a working development environment

**Acceptance Criteria**:
- ✅ Create project directory structure
- ✅ Create `requirements.txt` with Rich library
- ✅ Install dependencies (`pip install rich`)
- ✅ Create placeholder Python files (main.py, game_engine.py, item_pool.py)
- ✅ Verify Rich library works with a "Hello World" test
- ✅ Create `.gitignore` for Python projects
- ✅ Initialize Git repository (optional)

**Technical Implementation**:
```bash
# Directory structure
forgetwingame/
├── main.py
├── game_engine.py
├── item_pool.py
├── requirements.txt
├── README.md
└── docs/
    ├── prd/
    ├── architecture/
    └── EPICS_STORIES.md
```

**requirements.txt**:
```
rich>=13.0.0
```

**Test**:
```python
# test_rich.py
from rich.console import Console
console = Console()
console.print("[bold cyan]Rich library is working![/bold cyan]")
```

**Story Points**: 2  
**Priority**: P0  
**Dependencies**: None  
**Status**: 🔵 Ready

---

### **Story 1.2: Item Pool Data Structure**

**As a** developer  
**I want to** create the item pool with 8 thematic categories  
**So that** the game has diverse, meaningful content

**Acceptance Criteria**:
- ✅ Create `Item` dataclass with fields: text, is_good, category
- ✅ Define `ITEM_THEMES` dictionary with 8 categories
- ✅ Implement 80 total items (40 good, 40 bad)
- ✅ Each category has 5 good and 5 bad items
- ✅ Items are thematically appropriate and meaningful
- ✅ `ItemPool` class can build item list from themes

**Technical Implementation**:
```python
# item_pool.py
from dataclasses import dataclass
from typing import List, Dict, Tuple
import random

@dataclass
class Item:
    """Represents a game item"""
    text: str          # "Water", "Soda", etc.
    is_good: bool      # True for ✅, False for ❌
    category: str      # "healthy_habits", etc.
    
    def __str__(self):
        symbol = "✅" if self.is_good else "❌"
        return f"{symbol}  {self.text}"

class ItemPool:
    """Manages all game items organized by theme"""
    
    ITEM_THEMES = {
        "healthy_habits": {
            "good": ["Water", "Exercise", "Sleep", "Salad", "Meditation"],
            "bad": ["Soda", "Junk Food", "Stress", "Scrolling", "All-nighter"]
        },
        "productivity": {
            "good": ["Task Done", "Deep Work", "Study", "Plan", "Focus"],
            "bad": ["Procrastinate", "Multitask", "Gaming", "Distraction", "Busy Work"]
        },
        # ... 6 more categories (see PRD for full list)
    }
    
    def __init__(self):
        self.all_items: List[Item] = self._build_item_pool()
    
    def _build_item_pool(self) -> List[Item]:
        """Build list of all items from themes"""
        items = []
        for category, theme_items in self.ITEM_THEMES.items():
            for text in theme_items["good"]:
                items.append(Item(text, True, category))
            for text in theme_items["bad"]:
                items.append(Item(text, False, category))
        return items
```

**Test**:
```python
# Test item pool creation
pool = ItemPool()
assert len(pool.all_items) == 80
assert len([i for i in pool.all_items if i.is_good]) == 40
assert len([i for i in pool.all_items if not i.is_good]) == 40
print("✅ Item pool created successfully!")
```

**Story Points**: 3  
**Priority**: P0  
**Dependencies**: Story 1.1  
**Status**: 🔵 Ready

---

### **Story 1.3: Item Selection & Shuffling Logic**

**As a** developer  
**I want to** implement item selection and shuffling methods  
**So that** each level gets random, non-repeating items

**Acceptance Criteria**:
- ✅ `get_level_items(num_good, num_bad)` returns random items
- ✅ No duplicate items within a single level
- ✅ Items are randomly sampled from the pool
- ✅ `shuffle_display_items()` randomizes item order
- ✅ Method works for all level configurations (3-7 good, 2-6 bad)

**Technical Implementation**:
```python
# item_pool.py (continued)
class ItemPool:
    # ... (previous code)
    
    def get_level_items(
        self,
        num_good: int,
        num_bad: int,
        preferred_themes: List[str] = None
    ) -> Tuple[List[Item], List[Item]]:
        """
        Get random items for a level
        
        Args:
            num_good: Number of good items to select
            num_bad: Number of bad items to select
            preferred_themes: Optional list of themes to prefer
        
        Returns:
            (good_items, bad_items) tuple
        """
        # Filter by type
        good_pool = [item for item in self.all_items if item.is_good]
        bad_pool = [item for item in self.all_items if not item.is_good]
        
        # Optional theme filtering
        if preferred_themes:
            good_pool = [i for i in good_pool if i.category in preferred_themes]
            bad_pool = [i for i in bad_pool if i.category in preferred_themes]
        
        # Random selection (no duplicates)
        good_items = random.sample(good_pool, num_good)
        bad_items = random.sample(bad_pool, num_bad)
        
        return good_items, bad_items
    
    @staticmethod
    def shuffle_display_items(
        good_items: List[Item],
        bad_items: List[Item]
    ) -> List[Item]:
        """
        Combine and shuffle items for display
        
        Args:
            good_items: List of good items
            bad_items: List of bad items
        
        Returns:
            Shuffled list of all items
        """
        all_items = good_items + bad_items
        random.shuffle(all_items)
        return all_items
```

**Test**:
```python
# Test item selection
pool = ItemPool()
good, bad = pool.get_level_items(3, 2)
assert len(good) == 3
assert len(bad) == 2
assert all(i.is_good for i in good)
assert all(not i.is_good for i in bad)

# Test shuffling
shuffled = ItemPool.shuffle_display_items(good, bad)
assert len(shuffled) == 5
assert set(shuffled) == set(good + bad)
print("✅ Item selection and shuffling work!")
```

**Story Points**: 3  
**Priority**: P0  
**Dependencies**: Story 1.2  
**Status**: 🔵 Ready

---

## 🎮 Epic 2: Core Game Engine

**Goal**: Implement game logic, level management, and state tracking

**Priority**: P0 (Critical)  
**Total Story Points**: 13  
**Dependencies**: Epic 1  
**Estimated Duration**: 2-3 days

---

### **Story 2.1: Game Configuration & Constants**

**As a** developer  
**I want to** define game configuration and constants  
**So that** game difficulty and scoring are centralized

**Acceptance Criteria**:
- ✅ Create `GameConfig` dataclass with all constants
- ✅ Define 5 level configurations (items, time, distractors)
- ✅ Define scoring constants (points, penalties, multiplier)
- ✅ Define 6 rank tiers with thresholds
- ✅ Configuration is immutable and accessible

**Technical Implementation**:
```python
# game_engine.py
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class GameConfig:
    """Configuration for game difficulty and progression"""
    
    # Level configurations
    LEVELS = {
        1: {"good_items": 3, "bad_items": 2, "display_time": 10, "distractors": []},
        2: {"good_items": 4, "bad_items": 3, "display_time": 8, "distractors": []},
        3: {"good_items": 5, "bad_items": 4, "display_time": 7, "distractors": []},
        4: {"good_items": 6, "bad_items": 5, "display_time": 6, "distractors": ["visual_camouflage"]},
        5: {"good_items": 7, "bad_items": 6, "display_time": 5, "distractors": ["visual_camouflage", "temporal_interference"]},
    }
    
    # Scoring constants
    POINTS_PER_CORRECT_GOOD = 10
    PENALTY_PER_FORGOTTEN_GOOD = 5
    PENALTY_PER_REMEMBERED_BAD = 3
    STREAK_MULTIPLIER = 0.2
    
    # Rank thresholds
    RANKS = [
        (0, 20, "Information Overloaded", "🤯", "Your brain needs a reboot"),
        (21, 40, "Digital Hoarder", "📦", "Still holding onto junk data"),
        (41, 60, "Selective Learner", "🎓", "Getting the hang of it"),
        (61, 80, "Focus Ninja", "🥷", "Distractions fear you"),
        (81, 95, "Zen Master", "🧘", "Mind like water"),
        (96, 100, "Cognitive Elite", "👑", "You've achieved mental clarity"),
    ]
```

**Test**:
```python
# Test configuration access
config = GameConfig.LEVELS[1]
assert config["good_items"] == 3
assert config["display_time"] == 10

points = GameConfig.POINTS_PER_CORRECT_GOOD
assert points == 10

ranks = GameConfig.RANKS
assert len(ranks) == 6
print("✅ Game configuration defined!")
```

**Story Points**: 2  
**Priority**: P0  
**Dependencies**: Epic 1  
**Status**: 🔵 Ready

---

### **Story 2.2: Scoring Calculator**

**As a** developer  
**I want to** implement scoring calculation logic  
**So that** player performance is accurately evaluated

**Acceptance Criteria**:
- ✅ `calculate_level_score()` returns (base, bonus, total)
- ✅ Base score formula: (correct×10) - (forgotten×5) - (wrong×3)
- ✅ Streak bonus formula: base × (streak × 0.2)
- ✅ Base score cannot be negative (min = 0)
- ✅ `calculate_accuracy()` returns percentage
- ✅ `get_rank()` returns rank info based on score

**Technical Implementation**:
```python
# game_engine.py (continued)
class ScoreCalculator:
    """Handles all scoring logic"""
    
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
    
    @staticmethod
    def calculate_accuracy(
        correct_good: int,
        total_good: int,
        remembered_bad: int,
        total_bad: int
    ) -> float:
        """Calculate accuracy percentage"""
        total_items = total_good + total_bad
        correct_items = correct_good + (total_bad - remembered_bad)
        return (correct_items / total_items * 100) if total_items > 0 else 0
    
    @staticmethod
    def get_rank(score: int) -> Tuple[str, str, str, int]:
        """
        Get rank information based on score
        
        Returns:
            (rank_name, badge, tagline, next_rank_points)
        """
        for i, (min_score, max_score, name, badge, tagline) in enumerate(GameConfig.RANKS):
            if min_score <= score <= max_score:
                # Calculate points to next rank
                if i < len(GameConfig.RANKS) - 1:
                    next_rank_min = GameConfig.RANKS[i + 1][0]
                    points_needed = next_rank_min - score
                else:
                    points_needed = 0  # Already at max rank
                
                return name, badge, tagline, points_needed
        
        # Fallback for scores > 100
        return GameConfig.RANKS[-1][2], GameConfig.RANKS[-1][3], GameConfig.RANKS[-1][4], 0
```

**Test**:
```python
# Test scoring
base, bonus, total = ScoreCalculator.calculate_level_score(
    correct_good=3, total_good=3, remembered_bad=0, streak=0
)
assert base == 30  # 3 * 10
assert bonus == 0  # No streak
assert total == 30

# Test accuracy
accuracy = ScoreCalculator.calculate_accuracy(3, 3, 0, 2)
assert accuracy == 100.0

# Test rank
name, badge, tagline, points = ScoreCalculator.get_rank(30)
assert name == "Digital Hoarder"
print("✅ Scoring calculator works!")
```

**Story Points**: 4  
**Priority**: P0  
**Dependencies**: Story 2.1  
**Status**: 🔵 Ready

---

### **Story 2.3: Level Manager & State Tracking**

**As a** developer  
**I want to** implement level state management  
**So that** game progression is tracked correctly

**Acceptance Criteria**:
- ✅ `LevelManager` tracks current_level, streak, total_score
- ✅ `start_level()` initializes level state
- ✅ `complete_level()` updates state and history
- ✅ `get_level_config()` returns level configuration
- ✅ Streak increments on 80%+ accuracy, resets otherwise
- ✅ Level results are stored in history

**Technical Implementation**:
```python
# game_engine.py (continued)
from dataclasses import dataclass
import time

@dataclass
class LevelResult:
    """Stores results from a single level"""
    level_number: int
    correct_good: int
    total_good: int
    incorrect_bad: int
    total_bad: int
    forgotten_good: int
    base_score: int
    streak_bonus: int
    total_score: int
    accuracy: float
    time_taken: float

class LevelManager:
    """Manages level progression and state"""
    
    def __init__(self):
        self.current_level: int = 1
        self.streak: int = 0
        self.total_score: int = 0
        self.level_results: List[LevelResult] = []
        self.start_time: float = None
    
    def get_level_config(self, level: int) -> Dict:
        """Get configuration for a specific level"""
        return GameConfig.LEVELS.get(level, GameConfig.LEVELS[5])
    
    def start_level(self, level: int):
        """Initialize a new level"""
        self.current_level = level
        self.start_time = time.time()
    
    def complete_level(self, result: LevelResult):
        """Process level completion"""
        self.level_results.append(result)
        self.total_score += result.total_score
        
        # Update streak
        if result.accuracy >= 80:  # 80% accuracy maintains streak
            self.streak += 1
        else:
            self.streak = 0
```

**Test**:
```python
# Test level manager
manager = LevelManager()
assert manager.current_level == 1
assert manager.streak == 0
assert manager.total_score == 0

# Test level start
manager.start_level(1)
assert manager.current_level == 1

# Test level completion
result = LevelResult(1, 3, 3, 0, 2, 0, 30, 0, 30, 100.0, 10.0)
manager.complete_level(result)
assert manager.total_score == 30
assert manager.streak == 1  # 100% >= 80%
print("✅ Level manager works!")
```

**Story Points**: 4  
**Priority**: P0  
**Dependencies**: Story 2.2  
**Status**: 🔵 Ready

---

### **Story 2.4: Timer & Countdown Logic**

**As a** developer  
**I want to** implement countdown timer for memorization phase  
**So that** players have limited time to memorize items

**Acceptance Criteria**:
- ✅ Timer counts down from display_time (5-10 seconds)
- ✅ Timer updates every second
- ✅ Timer displays remaining time
- ✅ Timer auto-advances when time expires
- ✅ Timer is accurate (uses time.sleep(1))

**Technical Implementation**:
```python
# game_engine.py (continued)
import time
from rich.console import Console

console = Console()

class GameDisplay:
    """Handles all visual display elements"""
    
    @staticmethod
    def show_countdown_timer(seconds: int):
        """Show animated countdown timer"""
        for i in range(seconds, 0, -1):
            # Calculate progress
            progress_pct = ((seconds - i) / seconds) * 100
            filled = int(progress_pct / 100 * 30)
            empty = 30 - filled
            
            # Color gradient
            if i > seconds * 0.66:
                color, emoji = "green", "🟢"
            elif i > seconds * 0.33:
                color, emoji = "yellow", "🟡"
            else:
                color, emoji = "red", "🔴"
            
            # Display progress bar
            bar = "█" * filled + "░" * empty
            console.print(
                f"\r{emoji} [{color}][{bar}] {int(progress_pct)}% [{color}] - [bold]{i}s remaining[/bold]",
                end=""
            )
            time.sleep(1)
        
        console.print()  # New line after timer
```

**Test**:
```python
# Test timer (manual verification)
print("Testing 5-second countdown:")
GameDisplay.show_countdown_timer(5)
print("✅ Timer completed!")
```

**Story Points**: 3  
**Priority**: P0  
**Dependencies**: Story 2.1  
**Status**: 🔵 Ready

---

## 📊 Epic 3: Scoring & Evaluation

**Goal**: Implement result display, feedback, and rank system

**Priority**: P0 (Critical)  
**Total Story Points**: 8  
**Dependencies**: Epic 2  
**Estimated Duration**: 1-2 days

---

### **Story 3.1: Level Result Display**

**As a** developer  
**I want to** display detailed level results  
**So that** players understand their performance

**Acceptance Criteria**:
- ✅ Display "LEVEL X COMPLETE!" header
- ✅ Show performance breakdown table
- ✅ Display correct/forgotten/wrong counts with points
- ✅ Show accuracy percentage
- ✅ Display base score and streak bonus
- ✅ Show total cumulative score
- ✅ Use Rich library for formatting

**Technical Implementation**:
```python
# game_engine.py (continued)
from rich.table import Table
from rich.panel import Panel

class LevelManager:
    # ... (previous code)
    
    def display_level_result(self, result: LevelResult):
        """Display beautiful level completion screen"""
        console.clear()
        
        # Header
        from rich.text import Text
        title = Text(f"🎉 LEVEL {result.level_number} COMPLETE! 🎉", style="bold cyan", justify="center")
        console.print("\n")
        console.print(title)
        console.print("\n")
        
        # Performance table
        table = Table(title="PERFORMANCE BREAKDOWN", show_header=False, box=None, padding=(0, 2))
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Points", style="yellow")
        
        table.add_row(
            "✅ Correctly Remembered:",
            f"{result.correct_good} / {result.total_good}",
            f"+{result.correct_good * GameConfig.POINTS_PER_CORRECT_GOOD} pts"
        )
        table.add_row(
            "❌ Incorrectly Remembered:",
            f"{result.incorrect_bad} / {result.total_bad}",
            f"-{result.incorrect_bad * GameConfig.PENALTY_PER_REMEMBERED_BAD} pts" if result.incorrect_bad > 0 else "+0 pts"
        )
        table.add_row(
            "😢 Forgotten Good Items:",
            f"{result.forgotten_good}",
            f"-{result.forgotten_good * GameConfig.PENALTY_PER_FORGOTTEN_GOOD} pts" if result.forgotten_good > 0 else "+0 pts"
        )
        table.add_row(
            "🎯 Accuracy:",
            f"{result.accuracy:.1f}%",
            ""
        )
        table.add_row("", "", "─────────")
        table.add_row(
            "💰 Level Score:",
            "",
            f"+{result.base_score} pts"
        )
        
        if result.streak_bonus > 0:
            table.add_row(
                f"🔥 Streak Bonus (x{self.streak}):",
                "",
                f"+{result.streak_bonus} pts"
            )
        
        table.add_row("", "", "═════════")
        table.add_row(
            "⭐ TOTAL SCORE:",
            "",
            f"[bold yellow]{self.total_score}[/bold yellow]"
        )
        
        console.print(Panel(table, border_style="green"))
        console.print("\n")
```

**Test**:
```python
# Test result display (visual verification)
manager = LevelManager()
result = LevelResult(1, 3, 3, 0, 2, 0, 30, 0, 30, 100.0, 10.0)
manager.complete_level(result)
manager.display_level_result(result)
input("Press ENTER to continue...")
```

**Story Points**: 3  
**Priority**: P0  
**Dependencies**: Story 2.3  
**Status**: 🔵 Ready

---

### **Story 3.2: Rank Display & Progress Bar**

**As a** developer  
**I want to** display player rank and progress  
**So that** players see their advancement

**Acceptance Criteria**:
- ✅ Display current rank with badge emoji
- ✅ Show progress bar to next rank
- ✅ Display points needed for next rank
- ✅ Progress bar is visual and accurate
- ✅ Handle max rank (no next rank)

**Technical Implementation**:
```python
# game_engine.py (continued)
class LevelManager:
    # ... (previous code in display_level_result)
    
    def display_level_result(self, result: LevelResult):
        # ... (previous table code)
        
        # Rank display
        rank_name, badge, tagline, points_needed = ScoreCalculator.get_rank(self.total_score)
        console.print(f"\n[bold cyan]Current Rank: {rank_name} {badge}[/bold cyan]", justify="center")
        
        if points_needed > 0:
            # Progress bar to next rank
            current_rank_min = next(r[0] for r in GameConfig.RANKS if r[2] == rank_name)
            next_rank_min = current_rank_min + points_needed
            progress_pct = ((self.total_score - current_rank_min) / points_needed) * 100
            
            filled = int(progress_pct / 100 * 30)
            bar = "█" * filled + "░" * (30 - filled)
            console.print(f"\n[{bar}] {self.total_score}/100", justify="center")
            console.print(f"[dim]{points_needed} points to next rank![/dim]", justify="center")
        
        console.print("\n")
```

**Test**:
```python
# Test rank display (visual verification)
manager = LevelManager()
manager.total_score = 45
rank_name, badge, tagline, points = ScoreCalculator.get_rank(45)
print(f"Rank: {rank_name} {badge}")
print(f"Points to next: {points}")
```

**Story Points**: 3  
**Priority**: P0  
**Dependencies**: Story 3.1  
**Status**: 🔵 Ready

---

### **Story 3.3: Final Results & Daily Wisdom**

**As a** developer  
**I want to** display final game results with educational tip  
**So that** players see overall performance and learn something

**Acceptance Criteria**:
- ✅ Display "GAME COMPLETE!" header
- ✅ Show final statistics (total score, accuracy, streak, time)
- ✅ Display final rank with badge and tagline
- ✅ Show star rating (1-5 based on score)
- ✅ Display random daily wisdom tip
- ✅ Show menu options (Play Again, High Scores, Quit)

**Technical Implementation**:
```python
# game_engine.py (continued)
class LevelManager:
    # ... (previous code)
    
    def display_final_results(self, total_time: float):
        """Display final game completion screen"""
        console.clear()
        
        # Header
        from rich.text import Text
        title = Text("🏆 GAME COMPLETE! 🏆", style="bold yellow", justify="center")
        console.print("\n")
        console.print(title)
        console.print("\n")
        
        # Statistics table
        table = Table(title="FINAL STATISTICS", show_header=False, box=None, padding=(0, 2))
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        overall_accuracy = sum(r.accuracy for r in self.level_results) / len(self.level_results)
        best_streak = max((r.level_number for r in self.level_results if r.accuracy >= 80), default=0)
        
        table.add_row("📊 Total Score:", f"{self.total_score} / 500")
        table.add_row("🎯 Overall Accuracy:", f"{overall_accuracy:.1f}%")
        table.add_row("🔥 Best Streak:", f"{best_streak} levels")
        table.add_row("⏱️  Total Time:", f"{int(total_time // 60)}m {int(total_time % 60)}s")
        
        console.print(Panel(table, border_style="yellow"))
        
        # Final rank
        rank_name, badge, tagline, _ = ScoreCalculator.get_rank(self.total_score)
        
        rank_panel = Panel(
            f"[bold yellow]{badge} {rank_name.upper()} {badge}[/bold yellow]\n\n"
            f'[dim]"{tagline}"[/dim]\n\n'
            f"{'⭐' * min(5, (self.total_score // 20) + 1)} ({min(5, (self.total_score // 20) + 1)}/5)",
            border_style="yellow",
            padding=(1, 4)
        )
        console.print("\n")
        console.print(rank_panel)
        
        # Daily wisdom
        import random
        daily_tips = [
            "Just like this game, your brain filters 99% of sensory input. Choose what to remember wisely.",
            "Productivity isn't about doing more—it's about forgetting the unimportant.",
            "Studies show: Writing a 'worry list' before bed helps your brain forget stress and sleep better.",
            "The Zeigarnik Effect: Your brain remembers unfinished tasks. Complete or consciously 'forget' them.",
            "Digital minimalism: Unsubscribe from 3 things today. Your attention is your most valuable asset.",
            "Cognitive load theory: Your working memory holds ~7 items. Forget the rest to think clearly.",
            "The 'Two-Minute Rule': If it takes <2 min, do it now. Otherwise, forget it or schedule it.",
            "Your brain's 'delete button' is sleep. 7-8 hours helps consolidate good memories, forget the noise.",
            "Decision fatigue is real. Automate small choices to save mental energy.",
            "The Pareto Principle: 80% of results come from 20% of efforts. Forget the low-impact 80%.",
        ]
        
        console.print("\n[bold cyan]💡 Daily Wisdom:[/bold cyan]")
        console.print(f'[italic]{random.choice(daily_tips)}[/italic]')
        console.print("\n")
```

**Test**:
```python
# Test final results (visual verification)
manager = LevelManager()
# Add some mock results
for i in range(1, 6):
    result = LevelResult(i, 3, 3, 0, 2, 0, 30, 0, 30, 100.0, 10.0)
    manager.complete_level(result)

manager.display_final_results(60.0)
input("Press ENTER to continue...")
```

**Story Points**: 2  
**Priority**: P0  
**Dependencies**: Story 3.2  
**Status**: 🔵 Ready

---

## 🎨 Epic 4: UI/UX Implementation

**Goal**: Implement Rich library integration, visual elements, and user interactions

**Priority**: P1 (High)  
**Total Story Points**: 13  
**Dependencies**: Epic 1, 2, 3  
**Estimated Duration**: 2-3 days

---

### **Story 4.1: Title Screen & ASCII Art**

**As a** developer  
**I want to** create an engaging title screen  
**So that** players are excited to start the game

**Acceptance Criteria**:
- ✅ Display large ASCII art logo "FORGET TO WIN"
- ✅ Show tagline: "Master the Art of Selective Forgetting"
- ✅ Use gradient colors (Magenta → Cyan → Blue → Yellow → Green)
- ✅ Show animated blinking prompt
- ✅ Wait for ENTER key press
- ✅ Clear screen before starting game

**Technical Implementation**:
```python
# game_engine.py (continued)
class GameDisplay:
    # ... (previous code)
    
    @staticmethod
    def show_title_screen():
        """Display enhanced game title screen with animations"""
        console.clear()
        
        # Animated entrance
        console.print("\n" * 3)
        
        title = """
[bold bright_cyan]╔══════════════════════════════════════════════════════════════════════╗[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                                                                      [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold magenta]███████╗ ██████╗ ██████╗  ██████╗ ███████╗████████╗[/bold magenta]            [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold magenta]██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝[/bold magenta]            [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold cyan]█████╗  ██║   ██║██████╔╝██║  ███╗█████╗     ██║[/bold cyan]               [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold cyan]██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝     ██║[/bold cyan]               [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold blue]██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗   ██║[/bold blue]               [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold blue]╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝[/bold blue]               [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                                                                      [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                    [bold yellow]████████╗ ██████╗[/bold yellow]                                [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                    [bold yellow]╚══██╔══╝██╔═══██╗[/bold yellow]                               [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                       [bold yellow]██║   ██║   ██║[/bold yellow]                               [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                       [bold yellow]██║   ██║   ██║[/bold yellow]                               [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                       [bold yellow]██║   ╚██████╔╝[/bold yellow]                               [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                       [bold yellow]╚═╝    ╚═════╝[/bold yellow]                                [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                                                                      [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold green]██╗    ██╗██╗███╗   ██╗[/bold green]                                         [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold green]██║    ██║██║████╗  ██║[/bold green]                                         [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold green]██║ █╗ ██║██║██╔██╗ ██║[/bold green]                                         [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold green]██║███╗██║██║██║╚██╗██║[/bold green]                                         [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]     [bold green]╚███╔███╔╝██║██║ ╚████║[/bold green]                                         [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]      [bold green]╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝[/bold green]                                         [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                                                                      [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]              [bold yellow]🧠 Master the Art of Selective Forgetting 🧠[/bold yellow]            [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                                                                      [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                  [dim]A Cognitive Training Experience[/dim]                      [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                                                                      [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]╚══════════════════════════════════════════════════════════════════════╝[/bold bright_cyan]
        """
        
        console.print(title)
        
        # Animated prompt
        for i in range(3):
            console.print("\n[bold bright_cyan]✨ Press ENTER to Begin Your Journey... ✨[/bold bright_cyan]", justify="center", end="\r")
            time.sleep(0.5)
            console.print(" " * 80, end="\r")
            time.sleep(0.3)
        
        console.print("\n[bold bright_cyan]✨ Press ENTER to Begin Your Journey... ✨[/bold bright_cyan]", justify="center")
        input()
```

**Test**:
```python
# Test title screen (visual verification)
GameDisplay.show_title_screen()
```

**Story Points**: 4  
**Priority**: P1  
**Dependencies**: Epic 2  
**Status**: 🔵 Ready

---

### **Story 4.2: Item Display Formatting**

**As a** developer  
**I want to** format items in a grid layout  
**So that** items are easy to read and visually appealing

**Acceptance Criteria**:
- ✅ `format_grid()` creates 3-column grid
- ✅ Good items displayed in green with ✅
- ✅ Bad items displayed in red with ❌
- ✅ Items are properly aligned
- ✅ Grid fits in 70-character width
- ✅ `format_recall_list()` creates numbered list without symbols

**Technical Implementation**:
```python
# item_pool.py (continued)
class ItemDisplay:
    """Handles item display formatting"""
    
    @staticmethod
    def format_grid(items: List[Item], columns: int = 3) -> str:
        """
        Format items in a grid layout
        
        Args:
            items: List of items to display
            columns: Number of columns (default 3)
        
        Returns:
            Formatted grid string
        """
        lines = []
        for i in range(0, len(items), columns):
            row_items = items[i:i+columns]
            row_parts = []
            
            for item in row_items:
                symbol = "✅" if item.is_good else "❌"
                color = "green" if item.is_good else "red"
                row_parts.append(f"[{color}]{symbol}  {item.text:<20}[/{color}]")
            
            lines.append("  " + "  ".join(row_parts))
        
        return "\n".join(lines)
    
    @staticmethod
    def format_recall_list(items: List[Item]) -> str:
        """
        Format items as numbered list for recall phase
        
        Args:
            items: List of items to display
        
        Returns:
            Formatted numbered list
        """
        lines = []
        for i, item in enumerate(items, 1):
            lines.append(f"  {i}. {item.text:<30}")
        
        return "\n".join(lines)
```

**Test**:
```python
# Test item formatting
pool = ItemPool()
good, bad = pool.get_level_items(3, 2)
all_items = ItemPool.shuffle_display_items(good, bad)

# Test grid
grid = ItemDisplay.format_grid(all_items)
console.print(grid)

# Test recall list
recall_list = ItemDisplay.format_recall_list(all_items)
console.print(recall_list)
```

**Story Points**: 3  
**Priority**: P1  
**Dependencies**: Story 1.3  
**Status**: 🔵 Ready

---

### **Story 4.3: Level Header Display**

**As a** developer  
**I want to** display level header with score  
**So that** players know their current progress

**Acceptance Criteria**:
- ✅ Display "🧠 FORGET TO WIN" title
- ✅ Show "Level: X/5"
- ✅ Show "Score: X"
- ✅ Use cyan borders
- ✅ Header fits in 70-character width

**Technical Implementation**:
```python
# game_engine.py (continued)
class GameDisplay:
    # ... (previous code)
    
    @staticmethod
    def show_level_header(level: int, score: int):
        """Display level header"""
        header = f"🧠 FORGET TO WIN                          Level: {level}/5  Score: {score}"
        console.print("┏" + "━" * 68 + "┓", style="cyan")
        console.print(f"┃  {header:<66}┃", style="cyan")
        console.print("┣" + "━" * 68 + "┫", style="cyan")
```

**Test**:
```python
# Test level header
GameDisplay.show_level_header(1, 0)
```

**Story Points**: 2  
**Priority**: P1  
**Dependencies**: Epic 2  
**Status**: 🔵 Ready

---

### **Story 4.4: Post-Game Menu**

**As a** developer  
**I want to** create a post-game menu  
**So that** players can play again or quit

**Acceptance Criteria**:
- ✅ Display fancy bordered menu box
- ✅ Show options: Play Again, High Scores, Quit
- ✅ Color-coded options (Green P, Yellow H, Red Q)
- ✅ Accept case-insensitive input
- ✅ Show loading animation when starting new game
- ✅ Display goodbye message when quitting

**Technical Implementation**:
```python
# main.py (to be created in next epic)
class ForgetToWinGame:
    # ... (other methods)
    
    def show_menu(self):
        """Show post-game menu with enhanced styling"""
        console.print("\n" * 2)
        
        # Create fancy menu panel
        menu_content = """
[bold bright_cyan]╔═══════════════════════════════════════════════════╗[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                                                   [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]  [bold yellow]🎮  What would you like to do?[/bold yellow]              [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                                                   [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]  [bold green]P[/bold green] [white]→[/white] [cyan]Play Again[/cyan]     [dim](Start a new game)[/dim]    [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]  [bold yellow]H[/bold yellow] [white]→[/white] [cyan]High Scores[/cyan]    [dim](View leaderboard)[/dim]    [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]  [bold red]Q[/bold red] [white]→[/white] [cyan]Quit[/cyan]           [dim](Exit the game)[/dim]       [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]║[/bold bright_cyan]                                                   [bold bright_cyan]║[/bold bright_cyan]
[bold bright_cyan]╚═══════════════════════════════════════════════════╝[/bold bright_cyan]
"""
        console.print(menu_content)
        
        from rich.prompt import Prompt
        choice = Prompt.ask(
            "\n[bold bright_cyan]➤ Choose an option[/bold bright_cyan]",
            choices=["p", "h", "q", "P", "H", "Q"],
            default="q"
        ).lower()
        
        if choice == "p":
            console.print("\n[bold green]🔄 Starting new game...[/bold green]\n")
            time.sleep(0.5)
            self.__init__()  # Reset game
            self.run()
        elif choice == "h":
            self.show_high_scores()
        else:
            console.print("\n[bold magenta]═══════════════════════════════════════════════════[/bold magenta]")
            console.print("[bold yellow]       Thanks for playing Forget to Win! 🧠✨[/bold yellow]")
            console.print("[bold magenta]═══════════════════════════════════════════════════[/bold magenta]\n")
    
    def show_high_scores(self):
        """Display high scores with enhanced styling"""
        console.clear()
        console.print("\n" * 3)
        console.print("[bold yellow]🏆 ═══════════════════════════════════════════════════ 🏆[/bold yellow]")
        console.print("[bold bright_cyan]                    HIGH SCORES[/bold bright_cyan]")
        console.print("[bold yellow]🏆 ═══════════════════════════════════════════════════ 🏆[/bold yellow]\n")
        console.print("[bold cyan]This feature is coming soon in v1.1![/bold cyan]")
        console.print("[dim]High scores will be saved and displayed here.[/dim]\n")
        console.print("[bold yellow]Press ENTER to return to menu...[/bold yellow]")
        input()
        self.show_menu()
```

**Test**:
```python
# Test menu (visual verification)
# Will be tested when main.py is created
```

**Story Points**: 4  
**Priority**: P1  
**Dependencies**: Epic 3  
**Status**: 🔵 Ready

---

## 📝 Implementation Order

### **Phase 1: Foundation** (Stories 1.1 - 1.3)
1. Story 1.1: Project Initialization
2. Story 1.2: Item Pool Data
3. Story 1.3: Item Selection Logic

**Deliverable**: Working item pool with 80 items

---

### **Phase 2: Game Logic** (Stories 2.1 - 2.4)
4. Story 2.1: Game Configuration
5. Story 2.2: Scoring Calculator
6. Story 2.3: Level Manager
7. Story 2.4: Timer Logic

**Deliverable**: Complete game engine

---

### **Phase 3: Feedback** (Stories 3.1 - 3.3)
8. Story 3.1: Level Results
9. Story 3.2: Rank Display
10. Story 3.3: Final Results

**Deliverable**: Complete feedback system

---

### **Phase 4: Polish** (Stories 4.1 - 4.4)
11. Story 4.1: Title Screen
12. Story 4.2: Item Formatting
13. Story 4.3: Level Header
14. Story 4.4: Post-Game Menu

**Deliverable**: Complete UI/UX

---

## ✅ Definition of Done

A story is considered **DONE** when:

1. **Code Complete**:
   - ✅ All acceptance criteria implemented
   - ✅ Code follows Python best practices
   - ✅ Type hints added where applicable
   - ✅ Docstrings added to all functions/classes

2. **Tested**:
   - ✅ Manual testing completed
   - ✅ Test cases pass (if applicable)
   - ✅ No errors or warnings

3. **Documented**:
   - ✅ Code is self-documenting
   - ✅ Complex logic has comments
   - ✅ README updated (if needed)

4. **Reviewed**:
   - ✅ Code reviewed by developer
   - ✅ Meets architecture guidelines
   - ✅ No technical debt introduced

---

## 🚀 Next Steps

**Ready to Start Implementation!**

**First Story**: Story 1.1 - Project Initialization & Dependencies

**Command to begin**:
```bash
cd forgetwingame
# Create requirements.txt
# Install dependencies
# Create placeholder files
```

---

**Let's start coding!** 🎮✨
