"""
Quick demo of the live countdown timer feature
"""
import time
import sys
from rich.console import Console

console = Console()

def demo_countdown():
    """Demonstrate the live countdown timer"""
    console.clear()
    console.print("\n[bold cyan]LIVE COUNTDOWN TIMER DEMO[/bold cyan]", justify="center")
    console.print("[dim]This is how the timer will look during the recall phase[/dim]", justify="center")
    console.print("\n")
    
    # Simulate a 10-second countdown
    total_time = 10
    
    # Initial display
    console.print("🟢 Time Remaining: [green]10s[/green]", justify="center")
    console.print("\n[yellow]Simulating user typing...[/yellow]", justify="center")
    
    for remaining in range(total_time - 1, -1, -1):
        time.sleep(1)
        
        # Color coding based on time remaining
        if remaining > total_time * 0.5:
            color = "green"
            icon = "🟢"
        elif remaining > total_time * 0.25:
            color = "yellow"
            icon = "🟡"
        else:
            color = "red"
            icon = "🔴"
        
        # Move cursor up and clear line, then print timer
        sys.stdout.write('\033[F\033[K')  # Move up and clear
        console.print(f"{icon} Time Remaining: [{color}]{remaining}s[/{color}]", justify="center")
    
    console.print("\n[bold red]⏰ TIME'S UP![/bold red]", justify="center")
    console.print("\n[dim]This is what players will see while typing their answers![/dim]", justify="center")

if __name__ == "__main__":
    demo_countdown()
