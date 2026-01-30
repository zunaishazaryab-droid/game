"""
Test the prompt_toolkit Application with live timer
This demonstrates the timer updating while the user types
"""
import time
import threading
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import WindowAlign
from prompt_toolkit.widgets import TextArea

def test_timer_app():
    """Test live timer with prompt_toolkit Application"""
    
    # Timer state
    total_time = 15
    time_remaining = [total_time]
    timer_active = [True]
    user_answer = [""]
    
    def countdown_timer():
        """Background countdown"""
        while time_remaining[0] > 0 and timer_active[0]:
            time.sleep(1)
            time_remaining[0] -= 1
        timer_active[0] = False
    
    def get_timer_text():
        """Generate timer display"""
        remaining = time_remaining[0]
        
        # Color coding
        if remaining > total_time * 0.5:
            icon = "🟢"
            bar = "█" * 20
        elif remaining > total_time * 0.25:
            icon = "🟡"
            filled = int((remaining / total_time) * 20)
            bar = "█" * filled + "░" * (20 - filled)
        else:
            icon = "🔴"
            filled = int((remaining / total_time) * 20)
            bar = "█" * filled + "░" * (20 - filled)
        
        return f"{icon} Time: {remaining}s [{bar}]"
    
    # Create timer display
    timer_control = FormattedTextControl(
        text=get_timer_text,
        focusable=False
    )
    
    timer_window = Window(
        content=timer_control,
        height=1,
        align=WindowAlign.CENTER
    )
    
    # Create input field
    input_field = TextArea(
        prompt="➤ ",
        multiline=False,
        focusable=True,
        focus_on_click=True
    )
    
    # Create instruction
    instruction_window = Window(
        content=FormattedTextControl(text="Type something and press Enter (you have 15 seconds)"),
        height=1,
        align=WindowAlign.CENTER
    )
    
    # Create layout
    root_container = HSplit([
        Window(height=1),
        timer_window,
        Window(height=1),
        instruction_window,
        input_field,
    ])
    
    layout = Layout(root_container)
    
    # Key bindings
    kb = KeyBindings()
    
    @kb.add('enter')
    def _(event):
        user_answer[0] = input_field.text
        timer_active[0] = False
        event.app.exit()
    
    @kb.add('c-c')
    def _(event):
        timer_active[0] = False
        event.app.exit()
    
    # Create app
    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=False,
        mouse_support=False
    )
    
    # Start timer
    timer_thread = threading.Thread(target=countdown_timer, daemon=True)
    timer_thread.start()
    
    # Auto-exit on timeout
    def check_timeout():
        while timer_active[0] and time_remaining[0] > 0:
            time.sleep(0.1)
            app.invalidate()  # Force redraw
        if time_remaining[0] <= 0:
            timer_active[0] = False
            app.exit()
    
    timeout_thread = threading.Thread(target=check_timeout, daemon=True)
    timeout_thread.start()
    
    # Run
    print("\n=== LIVE TIMER TEST ===")
    print("Watch the timer update while you type!\n")
    
    try:
        app.run()
    except KeyboardInterrupt:
        timer_active[0] = False
    
    # Show result
    print("\n")
    if time_remaining[0] <= 0 and not user_answer[0]:
        print("⏰ TIME'S UP! No input received.")
    elif time_remaining[0] <= 0:
        print(f"⏰ TIME'S UP! You typed: '{user_answer[0]}'")
    else:
        print(f"✓ You typed: '{user_answer[0]}' with {time_remaining[0]}s remaining!")
    
    print("\nThe timer was visible and updating while you typed!")

if __name__ == "__main__":
    test_timer_app()
