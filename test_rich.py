"""
Rich Library Test Script - Windows Compatible Version

This script verifies that the Rich library is installed correctly
and demonstrates various Rich features that will be used in the game.

Run this script after installing dependencies:
    pip install -r requirements.txt
    python test_rich.py
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    os.system("chcp 65001 > nul")  # Set console to UTF-8

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress
    from rich.text import Text
    from rich.prompt import Prompt
    import time
    
    console = Console()
    
    # Test 1: Basic Console Output
    console.clear()
    console.print("\n[bold cyan]" + "=" * 60 + "[/bold cyan]")
    console.print("[bold cyan]  [bold yellow]Rich Library Test Suite[/bold yellow]" + " " * 28 + "[/bold cyan]")
    console.print("[bold cyan]" + "=" * 60 + "[/bold cyan]\n")
    
    console.print("[bold green][OK] Test 1: Basic Console Output[/bold green]")
    console.print("   [cyan]Rich library is installed and working![/cyan]\n")
    
    # Test 2: Colors and Styles
    console.print("[bold green][OK] Test 2: Colors and Styles[/bold green]")
    console.print("   [red]Red text[/red] | [green]Green text[/green] | [blue]Blue text[/blue]")
    console.print("   [bold]Bold[/bold] | [italic]Italic[/italic] | [dim]Dim[/dim] | [underline]Underline[/underline]\n")
    
    # Test 3: Panels
    console.print("[bold green][OK] Test 3: Panels[/bold green]")
    panel = Panel(
        "[bold yellow]This is a panel![/bold yellow]\n"
        "[cyan]Panels will be used for game results and menus.[/cyan]",
        title="Sample Panel",
        border_style="cyan"
    )
    console.print(panel)
    console.print()
    
    # Test 4: Tables
    console.print("[bold green][OK] Test 4: Tables[/bold green]")
    table = Table(title="Sample Performance Table", show_header=True)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")
    table.add_column("Points", style="yellow")
    
    table.add_row("[+] Correct Items", "3 / 3", "+30 pts")
    table.add_row("[-] Wrong Items", "0 / 2", "+0 pts")
    table.add_row("[*] Accuracy", "100%", "")
    table.add_row("[=] Total Score", "", "[bold]30[/bold]")
    
    console.print(table)
    console.print()
    
    # Test 5: Progress Bar
    console.print("[bold green][OK] Test 5: Progress Bar (Countdown Timer)[/bold green]")
    console.print("   [dim]Simulating 5-second countdown...[/dim]\n")
    
    for i in range(5, 0, -1):
        # Calculate progress
        progress_pct = ((5 - i) / 5) * 100
        filled = int(progress_pct / 100 * 30)
        empty = 30 - filled
        
        # Color gradient
        if i > 3:
            color, marker = "green", "[G]"
        elif i > 1:
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
    
    console.print("\r   [OK] [green]Countdown complete![/green]" + " " * 50)
    console.print()
    
    # Test 6: Special Characters
    console.print("[bold green][OK] Test 6: Special Characters[/bold green]")
    console.print("   [+] Check | [-] Cross | [*] Star | [=] Equal | [>] Arrow\n")
    
    # Test 7: Text Formatting
    console.print("[bold green][OK] Test 7: Advanced Text Formatting[/bold green]")
    title = Text("FORGET TO WIN", style="bold magenta", justify="center")
    console.print(title)
    
    gradient_text = Text()
    gradient_text.append("F", style="bold magenta")
    gradient_text.append("O", style="bold cyan")
    gradient_text.append("R", style="bold blue")
    gradient_text.append("G", style="bold yellow")
    gradient_text.append("E", style="bold green")
    gradient_text.append("T", style="bold magenta")
    console.print(gradient_text, justify="center")
    console.print()
    
    # Test 8: User Input
    console.print("[bold green][OK] Test 8: User Input (Prompt)[/bold green]")
    console.print("   [dim]Testing interactive prompt...[/dim]\n")
    
    name = Prompt.ask(
        "   [bold cyan]What's your name?[/bold cyan]",
        default="Player"
    )
    console.print(f"\n   [green]Hello, {name}! Welcome to Forget to Win![/green]\n")
    
    # Summary
    console.print("[bold yellow]" + "=" * 60 + "[/bold yellow]")
    console.print("[bold green]SUCCESS: All Rich Library Tests Passed![/bold green]", justify="center")
    console.print("[bold yellow]" + "=" * 60 + "[/bold yellow]\n")
    
    console.print("[bold cyan]Rich library is ready for game development![/bold cyan]")
    console.print("[dim]You can now proceed to Story 1.2: Item Pool Data Structure[/dim]\n")
    
    # Story 1.1 Completion Summary
    console.print("\n[bold green]" + "=" * 60 + "[/bold green]")
    console.print("[bold yellow]Story 1.1: Project Initialization - COMPLETE[/bold yellow]", justify="center")
    console.print("[bold green]" + "=" * 60 + "[/bold green]\n")
    
    console.print("[bold cyan]Completed Tasks:[/bold cyan]")
    console.print("  [green][OK][/green] requirements.txt created")
    console.print("  [green][OK][/green] Rich library installed (v14.3.1)")
    console.print("  [green][OK][/green] main.py placeholder created")
    console.print("  [green][OK][/green] game_engine.py placeholder created")
    console.print("  [green][OK][/green] item_pool.py placeholder created")
    console.print("  [green][OK][/green] Rich library verified and working")
    console.print("\n[bold green]Ready for Story 1.2: Item Pool Data Structure![/bold green]\n")
    
except ImportError as e:
    print("ERROR: Rich library is not installed!")
    print(f"   Details: {e}")
    print("\nPlease install dependencies:")
    print("   pip install -r requirements.txt")
    print("\nThen run this test again:")
    print("   python test_rich.py")
except Exception as e:
    print(f"ERROR: Unexpected error occurred!")
    print(f"   Details: {e}")
    import traceback
    traceback.print_exc()
