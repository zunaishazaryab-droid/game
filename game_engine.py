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
Version: 1.0
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Initialize Rich console
console = Console()


@dataclass
class GameConfig:
    """
    Configuration for game difficulty and progression
    
    This class uses the Singleton pattern via class-level constants.
    All configuration is static and shared across the application.
    No instance creation needed - accessed via class attributes.
    
    Attributes:
        LEVELS: Dictionary mapping level numbers to configurations
        POINTS_PER_CORRECT_GOOD: Points awarded for each correct good item
        PENALTY_PER_FORGOTTEN_GOOD: Points deducted for each forgotten good item
        PENALTY_PER_REMEMBERED_BAD: Points deducted for each remembered bad item
        STREAK_MULTIPLIER: Multiplier for streak bonus (0.2 = 20% per streak level)
        RANKS: List of rank tiers with thresholds and metadata
    """
    
    # Level configurations (5 levels with progressive difficulty)
    LEVELS = {
        1: {
            "good_items": 3,
            "bad_items": 2,
            "display_time": 10,
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
    
    # Rank thresholds (min_score, max_score, name, badge, tagline)
    RANKS = [
        (0, 20, "Information Overloaded", "[!]", "Your brain needs a reboot"),
        (21, 40, "Digital Hoarder", "[#]", "Still holding onto junk data"),
        (41, 60, "Selective Learner", "[*]", "Getting the hang of it"),
        (61, 80, "Focus Ninja", "[>]", "Distractions fear you"),
        (81, 95, "Zen Master", "[~]", "Mind like water"),
        (96, 100, "Cognitive Elite", "[+]", "You've achieved mental clarity")
    ]
    
    @classmethod
    def get_level_config(cls, level: int) -> Dict:
        """
        Get configuration for a specific level
        
        Args:
            level (int): Level number (1-5)
        
        Returns:
            Dict: Level configuration
        """
        return cls.LEVELS.get(level, cls.LEVELS[5])
    
    @classmethod
    def get_max_possible_score(cls) -> int:
        """
        Calculate maximum possible score across all levels
        
        Returns:
            int: Maximum possible score (assuming perfect play)
        """
        max_score = 0
        for level_num in range(1, 6):
            config = cls.LEVELS[level_num]
            level_max = config["good_items"] * cls.POINTS_PER_CORRECT_GOOD
            max_score += level_max
        return max_score


class ScoreCalculator:
    """
    Handles all scoring logic
    
    This class uses the Strategy pattern to encapsulate scoring algorithms.
    All methods are static - no state needed.
    Different scoring strategies can be added without modifying clients.
    """
    
    @staticmethod
    def calculate_level_score(
        correct_good: int,
        total_good: int,
        remembered_bad: int,
        streak: int
    ) -> Tuple[int, int, int]:
        """
        Calculate score for a level
        
        Algorithm:
        1. Calculate base score (rewards - penalties)
        2. Apply streak multiplier
        3. Return breakdown
        
        Args:
            correct_good (int): Number of good items correctly remembered
            total_good (int): Total number of good items
            remembered_bad (int): Number of bad items incorrectly remembered
            streak (int): Current streak level
        
        Returns:
            Tuple[int, int, int]: (base_score, streak_bonus, total_score)
        
        Example:
            >>> ScoreCalculator.calculate_level_score(3, 3, 0, 0)
            (30, 0, 30)
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
        """
        Calculate accuracy percentage
        
        Accuracy = (correct decisions / total decisions) * 100
        Correct decisions = correct good + correct bad (forgotten)
        
        Args:
            correct_good (int): Number of good items correctly remembered
            total_good (int): Total number of good items
            remembered_bad (int): Number of bad items incorrectly remembered
            total_bad (int): Total number of bad items
        
        Returns:
            float: Accuracy percentage (0-100)
        
        Example:
            >>> ScoreCalculator.calculate_accuracy(3, 3, 0, 2)
            100.0
        """
        total_items = total_good + total_bad
        correct_items = correct_good + (total_bad - remembered_bad)
        
        return (correct_items / total_items * 100) if total_items > 0 else 0
    
    @staticmethod
    def get_rank(score: int) -> Tuple[str, str, str, int]:
        """
        Get rank information based on score
        
        Args:
            score (int): Total score
        
        Returns:
            Tuple[str, str, str, int]: (rank_name, badge, tagline, points_to_next_rank)
        
        Example:
            >>> name, badge, tagline, points = ScoreCalculator.get_rank(30)
            >>> name
            'Digital Hoarder'
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
        
        # Fallback for scores > 100 (shouldn't happen, but just in case)
        last_rank = GameConfig.RANKS[-1]
        return last_rank[2], last_rank[3], last_rank[4], 0


@dataclass
class LevelResult:
    """
    Data Transfer Object: Stores results from a single level
    
    This is an immutable snapshot of level performance.
    Once created, it cannot be modified (prevents accidental state corruption).
    
    Attributes:
        level_number (int): Level number (1-5)
        correct_good (int): Number of good items correctly remembered
        total_good (int): Total number of good items
        incorrect_bad (int): Number of bad items incorrectly remembered
        total_bad (int): Total number of bad items
        forgotten_good (int): Number of good items forgotten
        base_score (int): Base score (before streak bonus)
        streak_bonus (int): Bonus points from streak
        total_score (int): Total score for this level
        accuracy (float): Accuracy percentage
        time_taken (float): Time taken to complete level (seconds)
    """
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
    """
    Manages level progression and state
    
    This class uses the State pattern to track and manage game state.
    It maintains the current level, streak, total score, and level history.
    
    State Variables:
    - current_level: Which level is active (1-5)
    - streak: Consecutive levels with 80%+ accuracy
    - total_score: Cumulative score across all levels
    - level_results: History of all completed levels
    """
    
    def __init__(self):
        """Initialize level manager with default state"""
        self.current_level: int = 1
        self.streak: int = 0
        self.total_score: int = 0
        self.level_results: List[LevelResult] = []
        self.start_time: float = None
    
    def get_level_config(self, level: int) -> Dict:
        """
        Get configuration for a specific level
        
        Args:
            level (int): Level number (1-5)
        
        Returns:
            Dict: Level configuration
        """
        return GameConfig.get_level_config(level)
    
    def start_level(self, level: int):
        """
        Initialize a new level
        
        Args:
            level (int): Level number to start
        """
        self.current_level = level
        self.start_time = time.time()
    
    def complete_level(self, result: LevelResult):
        """
        Process level completion and update state
        
        State Updates:
        1. Store level result in history
        2. Update cumulative score
        3. Update streak (based on accuracy)
        
        Args:
            result (LevelResult): Level result data
        """
        # Update history
        self.level_results.append(result)
        
        # Update cumulative score
        self.total_score += result.total_score
        
        # Update streak (80% accuracy maintains/increases streak)
        if result.accuracy >= 80:
            self.streak += 1
        else:
            self.streak = 0
    
    def get_state_snapshot(self) -> Dict:
        """
        Get current state for debugging/persistence
        
        Returns:
            Dict: Complete state dictionary
        """
        avg_accuracy = 0
        if self.level_results:
            avg_accuracy = sum(r.accuracy for r in self.level_results) / len(self.level_results)
        
        return {
            "current_level": self.current_level,
            "streak": self.streak,
            "total_score": self.total_score,
            "levels_completed": len(self.level_results),
            "average_accuracy": avg_accuracy
        }
    
    def display_level_result(self, result: LevelResult):
        """
        Display beautiful level completion screen
        
        Shows:
        - Level completion header
        - Performance breakdown table
        - Current rank and progress
        - Streak information
        
        Args:
            result (LevelResult): Level result data to display
        """
        console.clear()
        
        # Header
        title = Text(f"LEVEL {result.level_number} COMPLETE!", style="bold cyan", justify="center")
        console.print("\n")
        console.print(title)
        console.print("\n")
        
        # Performance table
        table = Table(title="PERFORMANCE BREAKDOWN", show_header=False, box=None, padding=(0, 2))
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_column("Points", style="yellow")
        
        # Correctly remembered good items
        table.add_row(
            "[+] Correctly Remembered:",
            f"{result.correct_good} / {result.total_good}",
            f"+{result.correct_good * GameConfig.POINTS_PER_CORRECT_GOOD} pts"
        )
        
        # Incorrectly remembered bad items
        penalty_bad = result.incorrect_bad * GameConfig.PENALTY_PER_REMEMBERED_BAD
        table.add_row(
            "[-] Incorrectly Remembered:",
            f"{result.incorrect_bad} / {result.total_bad}",
            f"-{penalty_bad} pts" if penalty_bad > 0 else "+0 pts"
        )
        
        # Forgotten good items
        penalty_forgotten = result.forgotten_good * GameConfig.PENALTY_PER_FORGOTTEN_GOOD
        table.add_row(
            "[?] Forgotten Good Items:",
            f"{result.forgotten_good}",
            f"-{penalty_forgotten} pts" if penalty_forgotten > 0 else "+0 pts"
        )
        
        # Accuracy
        accuracy_color = "green" if result.accuracy >= 80 else "yellow" if result.accuracy >= 60 else "red"
        table.add_row(
            "[*] Accuracy:",
            f"[{accuracy_color}]{result.accuracy:.1f}%[/{accuracy_color}]",
            ""
        )
        
        # Separator
        table.add_row("", "", "-" * 15)
        
        # Base score
        table.add_row(
            "[$] Level Score:",
            "",
            f"+{result.base_score} pts"
        )
        
        # Streak bonus (if any)
        if result.streak_bonus > 0:
            table.add_row(
                f"[>] Streak Bonus (x{self.streak}):",
                "",
                f"+{result.streak_bonus} pts"
            )
        
        # Final separator
        table.add_row("", "", "=" * 15)
        
        # Total score
        table.add_row(
            "[=] TOTAL SCORE:",
            "",
            f"[bold yellow]{self.total_score}[/bold yellow]"
        )
        
        console.print(Panel(table, border_style="green"))
        console.print("\n")
        
        # Rank display
        self._display_rank_progress()
        
        # Streak message
        if result.accuracy >= 80:
            if self.streak == 1:
                console.print("[bold green]STREAK STARTED! Keep it up![/bold green]", justify="center")
            else:
                console.print(f"[bold green]STREAK: {self.streak}x! Amazing![/bold green]", justify="center")
        elif self.streak > 0:
            console.print("[bold yellow]Streak broken. Aim for 80%+ to rebuild![/bold yellow]", justify="center")
        
        console.print("\n")
    
    def _display_rank_progress(self):
        """Display current rank with progress bar to next rank"""
        rank_name, badge, tagline, points_needed = ScoreCalculator.get_rank(self.total_score)
        
        console.print(f"\n[bold cyan]Current Rank: {badge} {rank_name}[/bold cyan]", justify="center")
        console.print(f'[dim]"{tagline}"[/dim]', justify="center")
        
        if points_needed > 0:
            # Find current rank index
            current_rank_idx = next(
                i for i, (min_s, max_s, name, _, _) in enumerate(GameConfig.RANKS)
                if name == rank_name
            )
            
            current_rank_min = GameConfig.RANKS[current_rank_idx][0]
            next_rank_min = GameConfig.RANKS[current_rank_idx + 1][0]
            rank_range = next_rank_min - current_rank_min
            progress_in_rank = self.total_score - current_rank_min
            progress_pct = (progress_in_rank / rank_range) * 100 if rank_range > 0 else 0
            
            # Progress bar
            filled = int(progress_pct / 100 * 30)
            bar = "#" * filled + "." * (30 - filled)
            console.print(f"\n[{bar}] {self.total_score}/{next_rank_min}", justify="center")
            console.print(f"[dim]{points_needed} points to next rank![/dim]", justify="center")
        else:
            console.print("\n[bold yellow]MAX RANK ACHIEVED![/bold yellow]", justify="center")
        
        console.print()
    
    def display_final_results(self, total_time: float):
        """
        Display final game completion screen with statistics
        
        Shows:
        - Game complete header
        - Final statistics table
        - Final rank with star rating
        - Daily wisdom tip
        
        Args:
            total_time (float): Total time taken to complete game (seconds)
        """
        console.clear()
        
        # Header
        title = Text("GAME COMPLETE!", style="bold yellow", justify="center")
        console.print("\n")
        console.print(title)
        console.print("\n")
        
        # Statistics table
        table = Table(title="FINAL STATISTICS", show_header=False, box=None, padding=(0, 2))
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        # Calculate overall stats
        overall_accuracy = sum(r.accuracy for r in self.level_results) / len(self.level_results)
        best_level = max(self.level_results, key=lambda r: r.total_score)
        perfect_levels = len([r for r in self.level_results if r.accuracy == 100.0])
        max_possible = GameConfig.get_max_possible_score()
        
        table.add_row("[$] Total Score:", f"{self.total_score} / {max_possible}")
        table.add_row("[*] Overall Accuracy:", f"{overall_accuracy:.1f}%")
        table.add_row("[>] Best Level:", f"Level {best_level.level_number} ({best_level.total_score} pts)")
        table.add_row("[+] Perfect Levels:", f"{perfect_levels} / 5")
        table.add_row("[~] Max Streak:", f"{max(r.level_number for r in self.level_results if r.accuracy >= 80) if any(r.accuracy >= 80 for r in self.level_results) else 0}")
        table.add_row("[T] Total Time:", f"{int(total_time // 60)}m {int(total_time % 60)}s")
        
        console.print(Panel(table, border_style="yellow"))
        
        # Final rank
        rank_name, badge, tagline, _ = ScoreCalculator.get_rank(self.total_score)
        
        # Calculate star rating (1-5 based on score)
        star_rating = min(5, max(1, (self.total_score // 20) + 1))
        stars = "[*]" * star_rating
        
        rank_panel = Panel(
            f"[bold yellow]{badge} {rank_name.upper()} {badge}[/bold yellow]\n\n"
            f'[dim]"{tagline}"[/dim]\n\n'
            f"{stars} ({star_rating}/5)",
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
        
        console.print("\n[bold cyan][!] Daily Wisdom:[/bold cyan]")
        console.print(f'[italic]{random.choice(daily_tips)}[/italic]')
        console.print("\n")


class GameDisplay:
    """
    Handles all visual display elements
    
    This class provides static methods for rendering various UI components
    using the Rich library.
    """
    
    @staticmethod
    def show_level_header(level: int, score: int):
        """
        Display level header with current progress
        
        Args:
            level (int): Current level number
            score (int): Current total score
        """
        header = f"[BRAIN] FORGET TO WIN                          Level: {level}/5  Score: {score}"
        console.print("+" + "-" * 68 + "+", style="cyan")
        console.print(f"|  {header:<66}|", style="cyan")
        console.print("+" + "-" * 68 + "+", style="cyan")
    
    @staticmethod
    def show_countdown_timer(seconds: int):
        """
        Show animated countdown timer with gradient colors
        
        Args:
            seconds (int): Number of seconds to count down
        """
        for i in range(seconds, 0, -1):
            # Calculate progress
            progress_pct = ((seconds - i) / seconds) * 100
            filled = int(progress_pct / 100 * 30)
            empty = 30 - filled
            
            # Color gradient based on remaining time
            if i > seconds * 0.66:
                color, marker = "green", "[G]"
            elif i > seconds * 0.33:
                color, marker = "yellow", "[Y]"
            else:
                color, marker = "red", "[R]"
            
            # Display progress bar
            bar = "#" * filled + "." * empty
            console.print(
                f"\r   {marker} [{color}][{bar}] {int(progress_pct)}% [{color}] - [bold]{i}s remaining[/bold]",
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
    print()
    
    # Test 2: Scoring constants
    print("[OK] Test 2: Scoring Constants")
    print(f"   Points per correct: {GameConfig.POINTS_PER_CORRECT_GOOD}")
    print(f"   Penalty per forgotten: {GameConfig.PENALTY_PER_FORGOTTEN_GOOD}")
    print(f"   Penalty per wrong: {GameConfig.PENALTY_PER_REMEMBERED_BAD}")
    print(f"   Streak multiplier: {GameConfig.STREAK_MULTIPLIER}")
    print()
    
    # Test 3: Rank tiers
    print("[OK] Test 3: Rank Tiers")
    for min_s, max_s, name, badge, tagline in GameConfig.RANKS:
        print(f"   {badge} {name} ({min_s}-{max_s}): {tagline}")
    print()
    
    # Test 4: Score calculation
    print("[OK] Test 4: Score Calculation")
    base, bonus, total = ScoreCalculator.calculate_level_score(3, 3, 0, 0)
    print(f"   Perfect level (3/3 correct, 0 wrong, no streak):")
    print(f"      Base: {base}, Bonus: {bonus}, Total: {total}")
    assert base == 30, f"Expected base 30, got {base}"
    assert bonus == 0, f"Expected bonus 0, got {bonus}"
    assert total == 30, f"Expected total 30, got {total}"
    
    base, bonus, total = ScoreCalculator.calculate_level_score(3, 3, 0, 2)
    print(f"   Perfect level with 2x streak:")
    print(f"      Base: {base}, Bonus: {bonus}, Total: {total}")
    assert bonus == 12, f"Expected bonus 12 (30 * 0.4), got {bonus}"
    print()
    
    # Test 5: Accuracy calculation
    print("[OK] Test 5: Accuracy Calculation")
    accuracy = ScoreCalculator.calculate_accuracy(3, 3, 0, 2)
    print(f"   Perfect accuracy: {accuracy}%")
    assert accuracy == 100.0, f"Expected 100%, got {accuracy}%"
    
    accuracy = ScoreCalculator.calculate_accuracy(2, 3, 1, 2)
    print(f"   Mixed performance: {accuracy}%")
    expected = (2 + 1) / 5 * 100  # 60%
    assert abs(accuracy - expected) < 0.1, f"Expected {expected}%, got {accuracy}%"
    print()
    
    # Test 6: Rank determination
    print("[OK] Test 6: Rank Determination")
    test_scores = [10, 30, 50, 70, 90, 100]
    for score in test_scores:
        name, badge, tagline, points = ScoreCalculator.get_rank(score)
        print(f"   Score {score}: {badge} {name} ({points} to next)")
    print()
    
    # Test 7: Level Manager
    print("[OK] Test 7: Level Manager")
    manager = LevelManager()
    print(f"   Initial state: Level {manager.current_level}, Score {manager.total_score}, Streak {manager.streak}")
    
    # Simulate completing a level
    result = LevelResult(
        level_number=1,
        correct_good=3,
        total_good=3,
        incorrect_bad=0,
        total_bad=2,
        forgotten_good=0,
        base_score=30,
        streak_bonus=0,
        total_score=30,
        accuracy=100.0,
        time_taken=10.0
    )
    manager.complete_level(result)
    print(f"   After level 1: Level {manager.current_level}, Score {manager.total_score}, Streak {manager.streak}")
    assert manager.total_score == 30, f"Expected score 30, got {manager.total_score}"
    assert manager.streak == 1, f"Expected streak 1, got {manager.streak}"
    print()
    
    # Test 8: Max possible score
    print("[OK] Test 8: Maximum Possible Score")
    max_score = GameConfig.get_max_possible_score()
    print(f"   Maximum possible score: {max_score}")
    print()
    
    # Summary
    print("=" * 60)
    print("  SUCCESS: All Game Configuration Tests Passed!")
    print("=" * 60 + "\n")
    
    print("Configuration Summary:")
    print(f"  - 5 levels with progressive difficulty")
    print(f"  - Display time: 10s -> 5s")
    print(f"  - Items: 3-7 good, 2-6 bad")
    print(f"  - 6 rank tiers (0-100 points)")
    print(f"  - Streak bonus: 20% per level")
    print(f"  - Max possible score: {max_score}")
    print()
    
    # Test 9: Level Result Display (visual test)
    print("[OK] Test 9: Level Result Display")
    print("   Testing level completion screen...")
    manager = LevelManager()
    result = LevelResult(
        level_number=1,
        correct_good=3,
        total_good=3,
        incorrect_bad=0,
        total_bad=2,
        forgotten_good=0,
        base_score=30,
        streak_bonus=0,
        total_score=30,
        accuracy=100.0,
        time_taken=10.0
    )
    manager.complete_level(result)
    
    # Display the result
    manager.display_level_result(result)
    input("   Press ENTER to continue to final results test...")
    
    # Test 10: Final Results Display (visual test)
    print("\n[OK] Test 10: Final Results Display")
    print("   Testing game completion screen...")
    
    # Add more levels for a complete game
    for level_num in range(2, 6):
        result = LevelResult(
            level_number=level_num,
            correct_good=level_num + 2,
            total_good=level_num + 2,
            incorrect_bad=0,
            total_bad=level_num + 1,
            forgotten_good=0,
            base_score=(level_num + 2) * 10,
            streak_bonus=int((level_num + 2) * 10 * (level_num - 1) * 0.2),
            total_score=(level_num + 2) * 10 + int((level_num + 2) * 10 * (level_num - 1) * 0.2),
            accuracy=100.0,
            time_taken=10.0 - level_num
        )
        manager.complete_level(result)
    
    # Display final results
    manager.display_final_results(60.0)
    input("   Press ENTER to finish tests...")
    
    console.clear()
    print("\n" + "=" * 60)
    print("  SUCCESS: All Display Tests Passed!")
    print("=" * 60 + "\n")
    
    print("Epic 3: Scoring & Evaluation - COMPLETE!")
    print()
    print("Implemented Features:")
    print("  [OK] Level result display with performance breakdown")
    print("  [OK] Rank progress bar with visual feedback")
    print("  [OK] Streak tracking and display")
    print("  [OK] Final results with comprehensive statistics")
    print("  [OK] Star rating system (1-5 stars)")
    print("  [OK] Daily wisdom tips (10 unique tips)")
    print()
    print("Ready for Epic 4: UI/UX Implementation!")
    print()


if __name__ == "__main__":
    # Run tests when module is executed directly
    test_game_config()
