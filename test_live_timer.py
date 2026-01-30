"""
Test script for live countdown timer with prompt_toolkit
This demonstrates the timer working alongside user input
"""
import time
import threading
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

console = Console()

def test_live_timer():
    """Test the live countdown timer with prompt_toolkit input"""
    console.clear()
    console.print("\n[bold cyan]LIVE TIMER TEST[/bold cyan]", justify="center")
    console.print("[dim]Testing prompt_toolkit with Rich Live display[/dim]", justify="center")
    console.print()
    
    # Timer configuration
    total_time = 10
    time_remaining = [total_time]
    timer_active = [True]
    user_answer = [""]
    input_complete = [False]
    
    def countdown_timer():
        """Background countdown"""
        while time_remaining[0] > 0 and not input_complete[0]:
            time.sleep(1)
            time_remaining[0] -= 1
        timer_active[0] = False
    
    def create_timer_display():
        """Create timer display"""
        remaining = time_remaining[0]
        
        # Color coding
        if remaining > total_time * 0.5:
            color = "green"
            icon = "🟢"
        elif remaining > total_time * 0.25:
            color = "yellow"
            icon = "🟡"
        else:
            color = "red"
            icon = "🔴"
        
        # Create timer table
        timer_table = Table.grid(expand=True)
        timer_table.add_column(justify="center")
        timer_table.add_row(f"{icon} Time Remaining: [{color}]{remaining}s[/{color}]")
        
        return Panel(
            timer_table,
            border_style=color,
            title="[bold]Timer[/bold]",
            expand=False
        )
    
    # Start countdown
    timer_thread = threading.Thread(target=countdown_timer, daemon=True)
    timer_thread.start()
    
    # Create live display
    with Live(create_timer_display(), console=console, refresh_per_second=2, transient=False) as live:
        def update_timer():
            """Update timer display"""
            while timer_active[0] and not input_complete[0]:
                live.update(create_timer_display())
                time.sleep(0.5)
        
        # Start display update
        display_thread = threading.Thread(target=update_timer, daemon=True)
        display_thread.start()
        
        # Give display time to initialize
        time.sleep(0.2)
        
        # Prompt style
        prompt_style = Style.from_dict({
            'prompt': '#00aa00 bold',
        })
        
        try:
            console.print("\n[bold cyan]Type something and press Enter (you have 10 seconds):[/bold cyan]")
            
            def get_input():
                try:
                    answer = prompt(
                        HTML('<ansiyellow>➤ </ansiyellow>'),
                        style=prompt_style
                    )
                    user_answer[0] = answer
                    input_complete[0] = True
                except:
                    input_complete[0] = True
            
            # Start input thread
            input_thread = threading.Thread(target=get_input, daemon=True)
            input_thread.start()
            
            # Wait for completion or timeout
            while not input_complete[0] and time_remaining[0] > 0:
                time.sleep(0.1)
            
            # Stop timer
            timer_active[0] = False
            input_complete[0] = True
            time.sleep(0.3)
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Interrupted![/bold red]")
            return
    
    # Show result
    console.print()
    if time_remaining[0] <= 0 and not user_answer[0]:
        console.print("[bold red]⏰ TIME'S UP! No input received.[/bold red]", justify="center")
    elif time_remaining[0] <= 0:
        console.print(f"[bold yellow]⏰ TIME'S UP! You typed: '{user_answer[0]}'[/bold yellow]", justify="center")
    else:
        console.print(f"[bold green]✓ You typed: '{user_answer[0]}' with {time_remaining[0]}s remaining![/bold green]", justify="center")
    
    console.print("\n[dim]The timer was visible while you typed![/dim]", justify="center")

if __name__ == "__main__":
    test_live_timer()
