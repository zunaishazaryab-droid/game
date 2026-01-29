"""
Forget to Win - Main Game Entry Point

This is the main entry point for the Forget to Win game.
It contains the ForgetToWinGame class and the complete game loop.

Author: Development Team
Version: 1.0
"""

import sys
import os
import time
import random

# Fix Windows console encoding
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from game_engine import (
    GameConfig,
    ScoreCalculator,
    LevelManager,
    LevelResult,
    GameDisplay,
    console
)
from item_pool import ItemPool, ItemDisplay

class ForgetToWinGame:
    """
    Main game controller
    
    This class orchestrates the entire game flow using the Controller pattern.
    It coordinates between modules (game_engine, item_pool) and manages
    the game lifecycle (start, play, end).
    """
    
    def __init__(self):
        """Initialize game with fresh state"""
        self.level_manager = LevelManager()
        self.item_pool = ItemPool()
        self.game_start_time = None
    
    def run(self):
        """
        Main game loop - Template Method pattern
        
        Flow:
        1. Show title screen
        2. Play all 5 levels
        3. Show final results
        4. Handle post-game menu
        """
        self.show_title_screen()
        self.game_start_time = time.time()
        
        # Play all 5 levels
        for level_num in range(1, 6):
            self.play_level(level_num)
        
        # Calculate total time
        total_time = time.time() - self.game_start_time
        
        # Show final results
        self.level_manager.display_final_results(total_time)
        
        # Post-game menu
        self.show_menu()
    
    def show_title_screen(self):
        """
        Display enhanced game title screen with animations
        
        Features:
        - Large text logo
        - Gradient colors
        - Animated prompt
        - Instructions
        """
        console.clear()
        console.print("\n" * 2)
        
        # Title with gradient effect (Windows-compatible - no special characters)
        console.print("[bold cyan]" + "=" * 64 + "[/bold cyan]")
        console.print()
        console.print("[bold magenta]    FFFFFFF   OOOOO   RRRRRR    GGGGG   EEEEEEE  TTTTTTT[/bold magenta]", justify="center")
        console.print("[bold magenta]    FF       OO   OO  RR   RR  GG       EE          TT   [/bold magenta]", justify="center")
        console.print("[bold cyan]    FFFF     OO   OO  RRRRRR   GG  GGG  EEEEE       TT   [/bold cyan]", justify="center")
        console.print("[bold cyan]    FF       OO   OO  RR  RR   GG   GG  EE          TT   [/bold cyan]", justify="center")
        console.print("[bold blue]    FF        OOOOO   RR   RR   GGGGG   EEEEEEE     TT   [/bold blue]", justify="center")
        console.print()
        console.print("[bold yellow]                TTTTTTT   OOOOO                   [/bold yellow]", justify="center")
        console.print("[bold yellow]                   TT    OO   OO                  [/bold yellow]", justify="center")
        console.print("[bold yellow]                   TT    OO   OO                  [/bold yellow]", justify="center")
        console.print("[bold yellow]                   TT    OO   OO                  [/bold yellow]", justify="center")
        console.print("[bold yellow]                   TT     OOOOO                   [/bold yellow]", justify="center")
        console.print()
        console.print("[bold green]     W     W  III  N   N[/bold green]", justify="center")
        console.print("[bold green]     W     W   I   NN  N[/bold green]", justify="center")
        console.print("[bold green]     W  W  W   I   N N N[/bold green]", justify="center")
        console.print("[bold green]     WW   WW   I   N  NN[/bold green]", justify="center")
        console.print("[bold green]     W     W  III  N   N[/bold green]", justify="center")
        console.print()
        console.print("[bold yellow]         Master the Art of Selective Forgetting[/bold yellow]", justify="center")
        console.print()
        console.print("[bold cyan]" + "=" * 64 + "[/bold cyan]")
        
        # Game instructions
        instructions = Panel(
            "[bold cyan]HOW TO PLAY:[/bold cyan]\n\n"
            "[green][+][/green] Remember the [green]GOOD[/green] items (marked with [green][+][/green])\n"
            "[red][-][/red] Forget the [red]BAD[/red] items (marked with [red][-][/red])\n\n"
            "[yellow]You'll see items for a few seconds, then recall the GOOD ones.[/yellow]\n\n"
            "[bold]5 Levels[/bold] | [bold]Progressive Difficulty[/bold] | [bold]Streak Bonuses[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )
        console.print("\n")
        console.print(instructions)
        
        # Animated prompt
        console.print("\n")
        for i in range(3):
            console.print("[bold bright_cyan]>>> Press ENTER to Begin Your Journey... <<<[/bold bright_cyan]", justify="center", end="\r")
            time.sleep(0.5)
            console.print(" " * 80, end="\r")
            time.sleep(0.3)
        
        console.print("[bold bright_cyan]>>> Press ENTER to Begin Your Journey... <<<[/bold bright_cyan]", justify="center")
        input()
    
    def play_level(self, level_num: int):
        """
        Play a single level
        
        Flow:
        1. Get level configuration
        2. Select random items
        3. Memorization phase (show items with symbols)
        4. Recall phase (user selects items)
        5. Calculate score
        6. Display results
        
        Args:
            level_num (int): Level number (1-5)
        """
        # Start level
        self.level_manager.start_level(level_num)
        config = self.level_manager.get_level_config(level_num)
        
        # Get random items
        good_items, bad_items = self.item_pool.get_level_items(
            config["good_items"],
            config["bad_items"]
        )
        
        # Memorization phase
        self.memorization_phase(level_num, good_items, bad_items, config["display_time"])
        
        # Recall phase
        selected_items = self.recall_phase(good_items, bad_items)
        
        # Calculate results
        result = self.calculate_level_result(
            level_num,
            good_items,
            bad_items,
            selected_items,
            config["display_time"]
        )
        
        # Update state and display
        self.level_manager.complete_level(result)
        self.level_manager.display_level_result(result)
        
        # Wait for user to continue (except on last level)
        if level_num < 5:
            input("\nPress ENTER to continue to next level...")
    
    def memorization_phase(self, level_num: int, good_items, bad_items, display_time: int):
        """
        Memorization phase - show items with symbols
        
        Args:
            level_num (int): Current level number
            good_items (List[Item]): Good items to remember
            bad_items (List[Item]): Bad items to forget
            display_time (int): Time to display items (seconds)
        """
        console.clear()
        
        # Show level header
        GameDisplay.show_level_header(level_num, self.level_manager.total_score)
        
        # Shuffle and display items
        all_items = ItemPool.shuffle_display_items(good_items, bad_items)
        grid = ItemDisplay.format_grid(all_items, columns=3)
        
        console.print("\n")
        console.print("[bold yellow]MEMORIZATION PHASE[/bold yellow]", justify="center")
        console.print("[dim]Remember the [green][+] GOOD[/green] items, Forget the [red][-] BAD[/red] items[/dim]", justify="center")
        console.print("\n")
        console.print(grid)
        console.print("\n")
        
        # Countdown timer
        GameDisplay.show_countdown_timer(display_time)
        
        console.print("\n[bold cyan]Time's up! Get ready to recall...[/bold cyan]", justify="center")
        time.sleep(1)
    
    def recall_phase(self, good_items, bad_items):
        """
        Recall phase - user selects items they remember
        
        Args:
            good_items (List[Item]): Good items (correct answers)
            bad_items (List[Item]): Bad items (should not select)
        
        Returns:
            Set[Item]: Items selected by user
        """
        console.clear()
        
        # Shuffle items again (different order)
        all_items = ItemPool.shuffle_display_items(good_items, bad_items)
        recall_list = ItemDisplay.format_recall_list(all_items)
        
        console.print("\n")
        console.print("[bold yellow]RECALL PHASE[/bold yellow]", justify="center")
        console.print("[dim]Select the numbers of the GOOD items you remember[/dim]", justify="center")
        console.print("\n")
        console.print(recall_list)
        console.print("\n")
        
        # Get user input
        while True:
            try:
                answer = Prompt.ask(
                    "[bold cyan]Enter item numbers (comma-separated, e.g., 1,3,5)[/bold cyan]",
                    default=""
                )
                
                if not answer.strip():
                    # User selected nothing
                    return set()
                
                # Parse input
                selected_indices = [int(x.strip()) - 1 for x in answer.split(',')]
                
                # Validate indices
                if any(i < 0 or i >= len(all_items) for i in selected_indices):
                    console.print("[bold red]Invalid item numbers! Please try again.[/bold red]")
                    continue
                
                # Map to items
                selected_items = {all_items[i] for i in selected_indices}
                return selected_items
                
            except ValueError:
                console.print("[bold red]Invalid format! Use comma-separated numbers (e.g., 1,3,5)[/bold red]")
            except KeyboardInterrupt:
                console.print("\n[bold red]Game interrupted![/bold red]")
                exit(0)
    
    def calculate_level_result(
        self,
        level_num: int,
        good_items,
        bad_items,
        selected_items,
        time_taken: float
    ) -> LevelResult:
        """
        Calculate level result from user selections
        
        Args:
            level_num (int): Level number
            good_items (List[Item]): Good items
            bad_items (List[Item]): Bad items
            selected_items (Set[Item]): Items selected by user
            time_taken (float): Time taken for level
        
        Returns:
            LevelResult: Complete level result data
        """
        # Convert to sets for comparison
        good_items_set = set(good_items)
        
        # Calculate metrics
        correct_good = len(selected_items & good_items_set)
        remembered_bad = len(selected_items - good_items_set)
        forgotten_good = len(good_items) - correct_good
        
        # Calculate score
        base_score, streak_bonus, total_score = ScoreCalculator.calculate_level_score(
            correct_good,
            len(good_items),
            remembered_bad,
            self.level_manager.streak
        )
        
        # Calculate accuracy
        accuracy = ScoreCalculator.calculate_accuracy(
            correct_good,
            len(good_items),
            remembered_bad,
            len(bad_items)
        )
        
        # Create result object
        return LevelResult(
            level_number=level_num,
            correct_good=correct_good,
            total_good=len(good_items),
            incorrect_bad=remembered_bad,
            total_bad=len(bad_items),
            forgotten_good=forgotten_good,
            base_score=base_score,
            streak_bonus=streak_bonus,
            total_score=total_score,
            accuracy=accuracy,
            time_taken=time_taken
        )
    
    def show_menu(self):
        """
        Show post-game menu with enhanced styling
        
        Options:
        - Play Again (P)
        - High Scores (H) - Coming soon
        - Quit (Q)
        """
        console.print("\n" * 2)
        
        # Create fancy menu panel
        menu_content = """
[bold cyan]================================================================[/bold cyan]
[bold cyan]                                                                [/bold cyan]
[bold yellow]  [?] What would you like to do?[/bold yellow]                              
[bold cyan]                                                                [/bold cyan]
[bold cyan]  [P] [white]->[/white] [green]Play Again[/green]     [dim](Start a new game)[/dim]            [/bold cyan]
[bold cyan]  [H] [white]->[/white] [yellow]High Scores[/yellow]    [dim](View leaderboard)[/dim]           [/bold cyan]
[bold cyan]  [Q] [white]->[/white] [red]Quit[/red]           [dim](Exit the game)[/dim]               [/bold cyan]
[bold cyan]                                                                [/bold cyan]
[bold cyan]================================================================[/bold cyan]
"""
        console.print(menu_content)
        
        choice = Prompt.ask(
            "\n[bold bright_cyan]>>> Choose an option[/bold bright_cyan]",
            choices=["p", "h", "q", "P", "H", "Q"],
            default="q"
        ).lower()
        
        if choice == "p":
            console.print("\n[bold green]Starting new game...[/bold green]\n")
            time.sleep(0.5)
            self.__init__()  # Reset game
            self.run()
        elif choice == "h":
            self.show_high_scores()
        else:
            self.show_goodbye()
    
    def show_high_scores(self):
        """Display high scores (placeholder for v1.1)"""
        console.clear()
        console.print("\n" * 3)
        console.print("[bold yellow]" + "=" * 60 + "[/bold yellow]")
        console.print("[bold bright_cyan]                    HIGH SCORES[/bold bright_cyan]", justify="center")
        console.print("[bold yellow]" + "=" * 60 + "[/bold yellow]\n")
        console.print("[bold cyan]This feature is coming soon in v1.1![/bold cyan]", justify="center")
        console.print("[dim]High scores will be saved and displayed here.[/dim]", justify="center")
        console.print("\n[bold yellow]Press ENTER to return to menu...[/bold yellow]", justify="center")
        input()
        self.show_menu()
    
    def show_goodbye(self):
        """Display goodbye message"""
        console.clear()
        console.print("\n" * 3)
        console.print("[bold magenta]" + "=" * 60 + "[/bold magenta]")
        console.print("[bold yellow]       Thanks for playing Forget to Win! [BRAIN][/bold yellow]", justify="center")
        console.print("[bold magenta]" + "=" * 60 + "[/bold magenta]\n")
        console.print("[bold cyan]Remember: Productivity isn't about doing more—[/bold cyan]", justify="center")
        console.print("[bold cyan]it's about forgetting the unimportant.[/bold cyan]", justify="center")
        console.print("\n[dim]See you next time![/dim]", justify="center")
        console.print("\n")


def main():
    """Main entry point"""
    try:
        game = ForgetToWinGame()
        game.run()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Game interrupted! Goodbye![/bold red]")
    except Exception as e:
        console.print(f"\n\n[bold red]An error occurred: {e}[/bold red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
