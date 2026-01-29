"""
Demo Script - Test Individual Components
Run this to see visual mockups and test scoring logic
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from game_engine import ScoreCalculator, GameConfig, LevelManager, GameDisplay
from item_pool import ItemPool, ItemDisplay

console = Console()


def demo_title_screen():
    """Demo: Title Screen"""
    console.print("\n[bold yellow]═══ DEMO 1: TITLE SCREEN ═══[/bold yellow]\n")
    GameDisplay.show_title_screen()


def demo_item_display():
    """Demo: Item Display Grid"""
    console.print("\n[bold yellow]═══ DEMO 2: ITEM DISPLAY ═══[/bold yellow]\n")
    
    pool = ItemPool()
    good_items, bad_items = pool.get_level_items(5, 4)
    
    # Show header
    GameDisplay.show_level_header(3, 245)
    
    console.print("┃                                                                    ┃", style="cyan")
    console.print("┃  [bold]📋 MEMORIZATION PHASE[/bold]                                             ┃", style="cyan")
    console.print("┃  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ┃", style="cyan")
    console.print("┃                                                                    ┃", style="cyan")
    
    # Display items
    all_items = ItemPool.shuffle_display_items(good_items, bad_items)
    grid = ItemDisplay.format_grid(all_items)
    
    for line in grid.split('\n'):
        console.print(f"┃{line}┃", style="cyan")
    
    console.print("┃                                                                    ┃", style="cyan")
    console.print("┃  [dim]💡 Remember the ✅ items. Forget the ❌ items![/dim]                    ┃", style="cyan")
    console.print("┃                                                                    ┃", style="cyan")
    console.print("┗" + "━" * 68 + "┛", style="cyan")
    
    input("\nPress ENTER to continue...")


def demo_scoring():
    """Demo: Scoring Algorithm"""
    console.clear()
    console.print("\n[bold yellow]═══ DEMO 3: SCORING ALGORITHM ═══[/bold yellow]\n")
    
    # Test scenarios
    scenarios = [
        {
            "name": "Perfect Score",
            "correct_good": 5,
            "total_good": 5,
            "remembered_bad": 0,
            "streak": 3
        },
        {
            "name": "Good Performance",
            "correct_good": 4,
            "total_good": 5,
            "remembered_bad": 1,
            "streak": 2
        },
        {
            "name": "Average Performance",
            "correct_good": 3,
            "total_good": 5,
            "remembered_bad": 2,
            "streak": 0
        },
        {
            "name": "Poor Performance",
            "correct_good": 2,
            "total_good": 5,
            "remembered_bad": 3,
            "streak": 0
        }
    ]
    
    table = Table(title="Scoring Examples", show_header=True, header_style="bold cyan")
    table.add_column("Scenario", style="cyan")
    table.add_column("Correct", justify="center")
    table.add_column("Forgot", justify="center")
    table.add_column("Wrong", justify="center")
    table.add_column("Base", justify="right")
    table.add_column("Bonus", justify="right")
    table.add_column("Total", justify="right", style="bold yellow")
    table.add_column("Accuracy", justify="right")
    
    for scenario in scenarios:
        base, bonus, total = ScoreCalculator.calculate_level_score(
            scenario["correct_good"],
            scenario["total_good"],
            scenario["remembered_bad"],
            scenario["streak"]
        )
        
        accuracy = ScoreCalculator.calculate_accuracy(
            scenario["correct_good"],
            scenario["total_good"],
            scenario["remembered_bad"],
            4  # Assuming 4 bad items
        )
        
        forgotten = scenario["total_good"] - scenario["correct_good"]
        
        table.add_row(
            scenario["name"],
            str(scenario["correct_good"]),
            str(forgotten),
            str(scenario["remembered_bad"]),
            f"+{base}",
            f"+{bonus}" if bonus > 0 else "0",
            str(total),
            f"{accuracy:.1f}%"
        )
    
    console.print(table)
    
    # Show rank progression
    console.print("\n[bold cyan]Rank Progression:[/bold cyan]\n")
    
    rank_table = Table(show_header=True, header_style="bold cyan")
    rank_table.add_column("Score Range", style="cyan")
    rank_table.add_column("Rank", style="yellow")
    rank_table.add_column("Badge", justify="center")
    rank_table.add_column("Tagline", style="dim")
    
    for min_score, max_score, name, badge, tagline in GameConfig.RANKS:
        rank_table.add_row(
            f"{min_score}-{max_score}",
            name,
            badge,
            tagline
        )
    
    console.print(rank_table)
    
    input("\nPress ENTER to continue...")


def demo_level_result():
    """Demo: Level Result Screen"""
    console.clear()
    console.print("\n[bold yellow]═══ DEMO 4: LEVEL RESULT SCREEN ═══[/bold yellow]\n")
    
    from game_engine import LevelResult
    
    # Create mock result
    result = LevelResult(
        level_number=3,
        correct_good=4,
        total_good=5,
        incorrect_bad=1,
        total_bad=4,
        forgotten_good=1,
        base_score=35,
        streak_bonus=35,
        total_score=70,
        accuracy=80.0,
        time_taken=7.0
    )
    
    # Create level manager and display result
    manager = LevelManager()
    manager.streak = 2
    manager.total_score = 315
    manager.display_level_result(result)
    
    input("\nPress ENTER to continue...")


def demo_final_results():
    """Demo: Final Results Screen"""
    console.clear()
    console.print("\n[bold yellow]═══ DEMO 5: FINAL RESULTS SCREEN ═══[/bold yellow]\n")
    
    from game_engine import LevelResult
    
    # Create mock level results
    manager = LevelManager()
    manager.total_score = 487
    
    results = [
        LevelResult(1, 3, 3, 0, 2, 0, 30, 0, 30, 100.0, 10.0),
        LevelResult(2, 4, 4, 0, 3, 0, 40, 8, 48, 100.0, 8.0),
        LevelResult(3, 4, 5, 1, 4, 1, 35, 35, 70, 80.0, 7.0),
        LevelResult(4, 5, 6, 1, 5, 1, 45, 54, 99, 83.3, 6.0),
        LevelResult(5, 6, 7, 0, 6, 1, 55, 66, 121, 92.3, 5.0),
    ]
    
    manager.level_results = results
    manager.display_final_results(272.0)  # 4m 32s
    
    input("\nPress ENTER to continue...")


def demo_item_themes():
    """Demo: Show all item themes"""
    console.clear()
    console.print("\n[bold yellow]═══ DEMO 6: ITEM THEMES ═══[/bold yellow]\n")
    
    pool = ItemPool()
    
    for theme, items in pool.ITEM_THEMES.items():
        console.print(f"\n[bold cyan]{theme.replace('_', ' ').title()}:[/bold cyan]")
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Good", style="green")
        table.add_column("Bad", style="red")
        
        max_len = max(len(items["good"]), len(items["bad"]))
        
        for i in range(max_len):
            good = f"✅ {items['good'][i]}" if i < len(items["good"]) else ""
            bad = f"❌ {items['bad'][i]}" if i < len(items["bad"]) else ""
            table.add_row(good, bad)
        
        console.print(table)
    
    input("\nPress ENTER to continue...")


def main():
    """Run all demos"""
    console.clear()
    
    welcome = Panel(
        "[bold cyan]Forget to Win - Component Demo[/bold cyan]\n\n"
        "This demo showcases all visual mockups and core functionality.\n"
        "Press ENTER to cycle through each demo.",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(welcome)
    input("\nPress ENTER to start...")
    
    demos = [
        ("Title Screen", demo_title_screen),
        ("Item Display", demo_item_display),
        ("Scoring Algorithm", demo_scoring),
        ("Level Result", demo_level_result),
        ("Final Results", demo_final_results),
        ("Item Themes", demo_item_themes),
    ]
    
    for name, demo_func in demos:
        try:
            demo_func()
        except KeyboardInterrupt:
            console.print("\n[yellow]Demo interrupted.[/yellow]")
            break
    
    console.clear()
    console.print("\n[bold green]✅ Demo Complete![/bold green]")
    console.print("\n[cyan]To play the full game, run:[/cyan] [bold]python main.py[/bold]\n")


if __name__ == "__main__":
    main()
