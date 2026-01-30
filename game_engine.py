"""
Forget to Win - Game Engine

This module contains the core game logic, scoring, state management,
and UI components.

Classes:
    - GameConfig: Static configuration for game difficulty and progression
    - ScoreCalculator: Handles all scoring logic
    - LevelManager: Manages level progression and state
    - GameDisplay: Handles all visual display elements
    - LevelResult: Data transfer object for level results

Author: Development Team
Version: 1.1
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.align import Align

# Initialize Rich console
console = Console()


@dataclass
class GameConfig:
    """
    Configuration for game difficulty and progression
    
    This class uses the Singleton pattern via class-level constants.
    All configuration is static and shared across the application.
    """
    
    # Level configurations (5 levels with progressive difficulty)
    LEVELS = {
        1: {
            "good_items": 3,
            "bad_items": 2,
            "display_time": 4,  # Modified to 4s based on user request (Original: 10)
            "distractors": []
        },
        2: {
            "good_items": 4,
            "bad_items": 3,
            "display_time": 8,
            "distractors": []
        },
        3: {
            "good_items": 5,
            "bad_items": 4,
            "display_time": 7,
            "distractors": []
        },
        4: {
            "good_items": 6,
            "bad_items": 5,
            "display_time": 6,
            "distractors": ["visual_camouflage"]
        },
        5: {
            "good_items": 7,
            "bad_items": 6,
            "display_time": 5,
            "distractors": ["visual_camouflage", "temporal_interference"]
        }
    }
    
    # Scoring constants
    POINTS_PER_CORRECT_GOOD = 10
    PENALTY_PER_FORGOTTEN_GOOD = 5
    PENALTY_PER_REMEMBERED_BAD = 3
    STREAK_MULTIPLIER = 0.2  # 20% bonus per streak level
    
    # Typing timer for recall phase (seconds per level)
    TYPING_TIME = {
        1: 20,  # 5 items total
        2: 30,  # 7 items total
        3: 40,  # 9 items total
        4: 50,  # 11 items total
        5: 60   # 13 items total
    }
    
    # Rank thresholds (min_score, max_score, name, badge, tagline)
    RANKS = [
        (0, 20, "Information Overloaded", "🤯", "Your brain needs a reboot"),
        (21, 40, "Digital Hoarder", "📦", "Still holding onto junk data"),
        (41, 60, "Selective Learner", "🎓", "Getting the hang of it"),
        (61, 80, "Focus Ninja", "🥷", "Distractions fear you"),
        (81, 95, "Zen Master", "🧘", "Mind like water"),
        (96, 100, "Cognitive Elite", "👑", "You've achieved mental clarity")
    ]
    
    @classmethod
    def get_level_config(cls, level: int) -> Dict:
        """Get configuration for a specific level"""
        return cls.LEVELS.get(level, cls.LEVELS[5])
    
    @classmethod
    def get_max_possible_score(cls) -> int:
        """Calculate maximum possible score across all levels"""
        max_score = 0
        for level_num in range(1, 6):
            config = cls.LEVELS[level_num]
            level_max = config["good_items"] * cls.POINTS_PER_CORRECT_GOOD
            max_score += level_max
        return max_score


class ScoreCalculator:
    """Handles all scoring logic using Strategy pattern"""
    
    @staticmethod
    def calculate_level_score(
        correct_good: int,
        total_good: int,
        remembered_bad: int,
        streak: int
    ) -> Tuple[int, int, int]:
        """
        Calculate score for a level
        Returns: (base_score, streak_bonus, total_score)
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
        
        # Streak bonus (20% per streak level)
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
        Returns: (rank_name, badge, tagline, points_to_next_rank)
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
        last_rank = GameConfig.RANKS[-1]
        return last_rank[2], last_rank[3], last_rank[4], 0


@dataclass
class LevelResult:
    """Data Transfer Object: Stores results from a single level"""
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
    """Manages level progression and state (State pattern)"""
    
    def __init__(self):
        """Initialize level manager with default state"""
        self.current_level: int = 1
        self.streak: int = 0
        self.total_score: int = 0
        self.level_results: List[LevelResult] = []
        self.start_time: float = None
    
    def get_level_config(self, level: int) -> Dict:
        return GameConfig.get_level_config(level)
    
    def start_level(self, level: int):
        self.current_level = level
        self.start_time = time.time()
    
    def complete_level(self, result: LevelResult):
        """Process level completion and update state"""
        # Update history
        self.level_results.append(result)
        
        # Update cumulative score
        self.total_score += result.total_score
        
        # Update streak (80% accuracy maintains/increases streak)
        if result.accuracy >= 80:
            self.streak += 1
        else:
            self.streak = 0
    
    def display_level_result(self, result: LevelResult):
        """Display beautiful level completion screen"""
        console.clear()
        
        # Header
        title = Panel(
            Text(f"LEVEL {result.level_number} COMPLETE!", justify="center", style="bold cyan"),
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 2)
        )
        console.print("\n")
        console.print(title, justify="center")
        console.print("\n")
        
        # Performance table
        table = Table(title="PERFORMANCE BREAKDOWN", show_header=False, box=box.ROUNDED, border_style="cyan", padding=(0, 2))
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Points", style="yellow")
        
        # Correctly remembered good items
        table.add_row(
            "[green]✔ Correctly Remembered:[/green]",
            f"{result.correct_good} / {result.total_good}",
            f"+{result.correct_good * GameConfig.POINTS_PER_CORRECT_GOOD} pts"
        )
        
        # Incorrectly remembered bad items
        penalty_bad = result.incorrect_bad * GameConfig.PENALTY_PER_REMEMBERED_BAD
        table.add_row(
            "[red]✖ Incorrectly Remembered:[/red]",
            f"{result.incorrect_bad} / {result.total_bad}",
            f"-{penalty_bad} pts" if penalty_bad > 0 else "+0 pts"
        )
        
        # Forgotten good items
        penalty_forgotten = result.forgotten_good * GameConfig.PENALTY_PER_FORGOTTEN_GOOD
        table.add_row(
            "[yellow]❓ Forgotten Good Items:[/yellow]",
            f"{result.forgotten_good}",
            f"-{penalty_forgotten} pts" if penalty_forgotten > 0 else "+0 pts"
        )
        
        # Accuracy
        accuracy_color = "green" if result.accuracy >= 80 else "yellow" if result.accuracy >= 60 else "red"
        table.add_row(
            "🎯 Accuracy:",
            f"[{accuracy_color}]{result.accuracy:.1f}%[/{accuracy_color}]",
            ""
        )
        
        # Separator
        table.add_section()
        
        # Base score
        table.add_row(
            "💰 Level Score:",
            "",
            f"[bold]{result.base_score} pts[/bold]"
        )
        
        # Streak bonus (if any)
        if result.streak_bonus > 0:
            table.add_row(
                f"🔥 Streak Bonus (x{self.streak}):",
                "",
                f"[bold yellow]+{result.streak_bonus} pts[/bold yellow]"
            )
        
        # Final separator
        table.add_section()
        
        # Total score
        table.add_row(
            "⭐ TOTAL SCORE:",
            "",
            f"[bold yellow]{self.total_score}[/bold yellow]"
        )
        
        console.print(table, justify="center")
        console.print("\n")
        
        # Rank display
        self._display_rank_progress()
        
        # Streak message
        if result.accuracy >= 80:
            if self.streak == 1:
                console.print(Panel("[bold green]STREAK STARTED! Keep it up![/bold green]", border_style="green", expand=False), justify="center")
            else:
                console.print(Panel(f"[bold green]STREAK: {self.streak}x! Amazing![/bold green]", border_style="green", expand=False), justify="center")
        elif self.streak > 0:
            console.print(Panel("[bold yellow]Streak broken. Aim for 80%+ to rebuild![/bold yellow]", border_style="yellow", expand=False), justify="center")
        
        console.print("\n")
    
    def _display_rank_progress(self):
        """Display current rank with progress bar to next rank"""
        rank_name, badge, tagline, points_needed = ScoreCalculator.get_rank(self.total_score)
        
        console.print(f"[bold cyan]Current Rank: {badge} {rank_name}[/bold cyan]", justify="center")
        console.print(f'[italic dim]"{tagline}"[/italic dim]', justify="center")
        
        if points_needed > 0:
            # Find current rank index
            current_rank_idx = next(
                i for i, (min_s, max_s, name, _, _) in enumerate(GameConfig.RANKS)
                if name == rank_name
            )
            
            # Safe next rank retrieval
            if current_rank_idx < len(GameConfig.RANKS) - 1:
                current_rank_min = GameConfig.RANKS[current_rank_idx][0]
                next_rank_min = GameConfig.RANKS[current_rank_idx + 1][0]
                
                # Calculate progress
                rank_range = next_rank_min - current_rank_min
                score_in_rank = self.total_score - current_rank_min
                # Ensure score_in_rank is non-negative (for degraded ranks)
                score_in_rank = max(0, score_in_rank)
                
                progress_pct = (score_in_rank / rank_range) * 100 if rank_range > 0 else 0
                progress_pct = min(100, max(0, progress_pct))
                
                # Progress bar
                width = 30
                filled = int(progress_pct / 100 * width)
                bar = "█" * filled + "░" * (width - filled)
                console.print(f"\n[{bar}] [bold]{self.total_score}[/bold]/{next_rank_min}", justify="center")
                console.print(f"[dim]{points_needed} points to next rank![/dim]", justify="center")
        else:
            console.print("\n[bold yellow]🏆 MAX RANK ACHIEVED! 🏆[/bold yellow]", justify="center")
        
        console.print()
    
    def display_final_results(self, total_time: float):
        """Display final game completion screen with statistics"""
        console.clear()
        
        # Header
        console.print("\n")
        console.print(Panel("[bold yellow]GAME COMPLETE![/bold yellow]", box=box.DOUBLE, border_style="yellow", width=40), justify="center")
        console.print("\n")
        
        # Statistics table
        table = Table(title="FINAL STATISTICS", show_header=False, box=box.ROUNDED, border_style="yellow", padding=(0, 2))
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        # Calculate overall stats
        if self.level_results:
            overall_accuracy = sum(r.accuracy for r in self.level_results) / len(self.level_results)
            best_level = max(self.level_results, key=lambda r: r.total_score)
            perfect_levels = len([r for r in self.level_results if r.accuracy == 100.0])
            max_streak = max(r.level_number for r in self.level_results if r.accuracy >= 80) if any(r.accuracy >= 80 for r in self.level_results) else 0
        else:
            overall_accuracy = 0
            best_level = None
            perfect_levels = 0
            max_streak = 0
            
        max_possible = GameConfig.get_max_possible_score()
        
        table.add_row("💰 Total Score:", f"[bold yellow]{self.total_score}[/bold yellow] / {max_possible}")
        table.add_row("🎯 Overall Accuracy:", f"{overall_accuracy:.1f}%")
        if best_level:
            table.add_row("🏆 Best Level:", f"Level {best_level.level_number} ({best_level.total_score} pts)")
        table.add_row("✨ Perfect Levels:", f"{perfect_levels} / 5")
        table.add_row("🔥 Max Streak:", f"{max_streak}")
        table.add_row("⏱ Total Time:", f"{int(total_time // 60)}m {int(total_time % 60)}s")
        
        console.print(table, justify="center")
        
        # Final rank
        rank_name, badge, tagline, _ = ScoreCalculator.get_rank(self.total_score)
        
        # Calculate star rating (1-5 based on score)
        # Assuming max score is approx 250-300 depending on streak
        # 0-50: 1 star, 51-100: 2 stars, 101-150: 3 stars, 151-200: 4 stars, 200+: 5 stars
        if self.total_score < 50: star_rating = 1
        elif self.total_score < 100: star_rating = 2
        elif self.total_score < 150: star_rating = 3
        elif self.total_score < 200: star_rating = 4
        else: star_rating = 5
        
        stars = "⭐" * star_rating
        
        rank_panel = Panel(
            f"[bold yellow]{badge} {rank_name.upper()} {badge}[/bold yellow]\n\n"
            f'[italic]"{tagline}"[/italic]\n\n'
            f"{stars} ({star_rating}/5)",
            border_style="yellow",
            padding=(1, 4),
            title="Final Rank"
        )
        console.print("\n")
        console.print(rank_panel, justify="center")
        
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
        
        console.print("\n[bold cyan]💡 Daily Wisdom:[/bold cyan]", justify="center")
        console.print(f'[italic]{random.choice(daily_tips)}[/italic]', justify="center")
        console.print("\n")


class GameDisplay:
    """Handles all visual display elements using Rich"""
    
    @staticmethod
    def show_level_header(level: int, score: int):
        """Display level header with current progress"""
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right", ratio=1)
        grid.add_row(f"[bold cyan]🧠 FORGET TO WIN[/bold cyan]", f"[yellow]Level: {level}/5  Score: {score}[/yellow]")
        
        console.print(Panel(grid, style="cyan", border_style="cyan", box=box.ROUNDED))
    
    @staticmethod
    def show_countdown_timer(seconds: int):
        """Show animated countdown timer with gradient colors"""
        for i in range(seconds, 0, -1):
            # Calculate progress
            progress_pct = ((seconds - i) / seconds) * 100
            
            # Color gradient based on remaining time
            if i > seconds * 0.66:
                color = "green"
            elif i > seconds * 0.33:
                color = "yellow"
            else:
                color = "red"
            
            # Display progress bar
            width = 30
            filled = int(progress_pct / 100 * width)
            # Use Block characters for smoother look
            bar = "█" * filled + "░" * (width - filled)
            
            console.print(
                f"\r   ⏳ [{color}][{bar}] {int(progress_pct)}% - [bold]{i}s remaining[/bold]   ",
                end=""
            )
            time.sleep(1)
        
        console.print()  # New line after timer


# Module-level test function
def test_game_config():
    """Test function to verify GameConfig functionality"""
    print("\n" + "=" * 60)
    print("  Game Configuration Test Suite")
    print("=" * 60 + "\n")
    
    # Test 1: Level configurations
    print("[OK] Test 1: Level Configurations")
    for level in range(1, 6):
        config = GameConfig.get_level_config(level)
        print(f"   Level {level}: {config['good_items']} good, {config['bad_items']} bad, {config['display_time']}s")
    
    # Verify Level 1 timer is 4s
    l1_config = GameConfig.get_level_config(1)
    if l1_config["display_time"] != 4:
        print(f"   [FAIL] Level 1 timer is {l1_config['display_time']}s, expected 4s")
    else:
        print("   [PASS] Level 1 timer is set to 4s")
        
    print()
    
    # Test 2: Scoring
    print("[OK] Test 2: Scoring Calculations")
    base, bonus, total = ScoreCalculator.calculate_level_score(3, 3, 0, 0)
    print(f"   Perfect score base: {base}, total: {total}")
    assert total == 30
    
    # Test 3: Ranks
    print("[OK] Test 3: Ranks")
    name, badge, _, _ = ScoreCalculator.get_rank(100)
    print(f"   Top rank: {badge} {name}")
    
    print("\n" + "=" * 60)
    print("  SUCCESS: Basic tests completed.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    test_game_config()
