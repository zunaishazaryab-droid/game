# Dynamic Typing Timer Implementation

## Overview
Implemented a dynamic typing timer for the recall phase that increases with level difficulty, giving players more time as they need to remember more items. **Now includes a live countdown display** that updates in real-time while the user is typing!

## Changes Made

### 1. PRD Updates (`docs/prd/index.md`)
- Updated **FR-5: Recall Phase** to include dynamic typing timer requirements
- Added specifications for:
  - Level-based time limits (20s to 60s)
  - Live countdown display ✅ **IMPLEMENTED**
  - Auto-submit on timeout
  - Rich UI integration

### 2. Game Engine Updates (`game_engine.py`)
- Added `TYPING_TIME` configuration to `GameConfig` class:
  ```python
  TYPING_TIME = {
      1: 20,  # 5 items total
      2: 30,  # 7 items total
      3: 40,  # 9 items total
      4: 50,  # 11 items total
      5: 60   # 13 items total
  }
  ```

### 3. Main Game Updates (`main.py`)
- Completely rewrote `recall_phase()` method with:
  - **Threading**: Parallel timer and input handling
  - **Dynamic Timer**: Level-based time limits from `GameConfig.TYPING_TIME`
  - **Live Countdown**: ✅ Real-time countdown display with color coding
  - **Auto-Submit**: Automatically evaluates input when timer expires
  - **Graceful Timeout**: Shows "TIME'S UP!" message and processes partial input
  - **Improved Error Handling**: Attempts to parse valid numbers even with formatting errors
  - **Visual Feedback**: Color-coded timer (🟢 Green → 🟡 Yellow → 🔴 Red)

## Technical Implementation

### Threading Architecture
```
Main Thread
├── Display recall items
├── Show timer message
├── Start Timer Thread (countdown)
├── Start Display Thread (live countdown) ✅ NEW
├── Start Input Thread (get user input)
└── Wait for completion or timeout
    ├── If timeout: Show "TIME'S UP!" message
    └── Process and validate input
```

### Live Countdown Display ✅
- **Updates every 0.5 seconds** for smooth animation
- **Color-coded indicators**:
  - 🟢 **Green**: More than 50% time remaining
  - 🟡 **Yellow**: 25-50% time remaining
  - 🔴 **Red**: Less than 25% time remaining
- **Format**: "🟢 Time Remaining: 15s"
- **Uses ANSI escape codes** to update in place without scrolling

### Timer Behavior
- **Level 1**: 20 seconds (5 total items: 3 good + 2 bad)
- **Level 2**: 30 seconds (7 total items: 4 good + 3 bad)
- **Level 3**: 40 seconds (9 total items: 5 good + 4 bad)
- **Level 4**: 50 seconds (11 total items: 6 good + 5 bad)
- **Level 5**: 60 seconds (13 total items: 7 good + 6 bad)

## User Experience
1. User sees recall items and timer announcement
2. **Live timer displays in a panel** above the input field
3. Timer counts down with color changes: 🟢 → 🟡 → 🔴
4. User can type while watching the timer update in real-time
5. If timer expires before completion:
   - Shows "⏰ TIME'S UP!" message
   - Evaluates whatever was typed
6. If user completes in time:
   - Shows "✓ Answer submitted!" message
   - Immediately processes answer

## Windows Compatibility ✅
- **Uses `prompt_toolkit`** instead of standard `input()` for non-blocking input
- **Rich.Live display** properly initialized before input starts
- **Threading architecture** allows timer and input to run simultaneously
- **ANSI escape codes** not needed - Rich handles all rendering
- **Tested on Windows** with proper terminal encoding

## Technical Details

### prompt_toolkit Integration
```python
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

# Non-blocking prompt with custom styling
answer = prompt(
    HTML('<ansiyellow>➤ </ansiyellow>'),
    style=prompt_style
)
```

### Rich.Live Display
```python
with Live(create_timer_display(), console=console, refresh_per_second=2) as live:
    # Timer updates automatically
    def update_timer():
        while timer_active:
            live.update(create_timer_display())
            time.sleep(0.5)
```

### Threading Model
```
Main Thread
├── Initialize Rich.Live display
├── Start Countdown Thread (updates time_remaining)
├── Start Display Thread (updates Rich.Live every 0.5s)
├── Start Input Thread (prompt_toolkit.prompt)
└── Wait for completion or timeout
    ├── Stop all threads
    └── Process result
```

## Testing

### Test the live timer independently:
```bash
python test_live_timer.py
```
This will show a 10-second countdown with a live input field.

### Play the full game:
```bash
python main.py
```
The timer will be visible during each recall phase!
