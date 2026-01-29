"""
Forget to Win - Item Pool

This module manages all game items organized by theme.

Classes:
    - Item: Dataclass representing a game item
    - ItemPool: Repository for all game items
    - ItemDisplay: Formatter for item display

Author: Development Team
Version: 1.0
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import random


@dataclass(frozen=True, eq=True)
class Item:
    """
    Represents a game item
    
    Attributes:
        text (str): Display text for the item (e.g., "Water", "Soda")
        is_good (bool): True for good items (✅), False for bad items (❌)
        category (str): Thematic category (e.g., "healthy_habits")
    """
    text: str
    is_good: bool
    category: str
    
    def __str__(self) -> str:
        """String representation with symbol"""
        symbol = "[+]" if self.is_good else "[-]"
        return f"{symbol}  {self.text}"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"Item('{self.text}', {self.is_good}, '{self.category}')"


class ItemPool:
    """
    Manages all game items organized by theme
    
    The item pool contains 80 items across 8 thematic categories:
    - Healthy Habits (10 items)
    - Productivity (10 items)
    - Code Quality (10 items)
    - Cybersecurity (10 items)
    - Financial Wisdom (10 items)
    - Critical Thinking (10 items)
    - Emotional Intelligence (10 items)
    - Learning (10 items)
    
    Each category has 5 good items and 5 bad items.
    """
    
    # Thematic item pairs (8 categories, 80 items total)
    ITEM_THEMES = {
        "healthy_habits": {
            "good": ["Water", "Exercise", "Sleep 8hrs", "Salad", "Meditation"],
            "bad": ["Soda", "Junk Food", "All-nighter", "Scrolling", "Stress"]
        },
        "productivity": {
            "good": ["Task Done", "Deep Work", "Study", "Plan Ahead", "Focus Time"],
            "bad": ["Procrastinate", "Multitask", "Gaming", "Distraction", "Busy Work"]
        },
        "code_quality": {
            "good": ["def function()", "Unit Test", "Code Review", "Git Commit", "Documentation"],
            "bad": ["funtion()", "No Tests", "Skip Review", "Force Push", "No Comments"]
        },
        "cybersecurity": {
            "good": ["HTTPS", "2FA", "Strong Password", "VPN", "Update Software"],
            "bad": ["HTTP", "Password123", "Public WiFi", "Old Version", "Click Link"]
        },
        "financial_wisdom": {
            "good": ["Save Money", "Invest", "Budget", "Emergency Fund", "Track Expenses"],
            "bad": ["Impulse Buy", "Gamble", "Max Credit", "No Savings", "Ignore Bills"]
        },
        "critical_thinking": {
            "good": ["Evidence-based", "Fact Check", "Ask Questions", "Research", "Verify Source"],
            "bad": ["Trust me bro", "Confirmation Bias", "Assume", "Ignore Data", "Echo Chamber"]
        },
        "emotional_intelligence": {
            "good": ["Pause & Think", "Listen First", "Empathy", "Self-aware", "Calm Response"],
            "bad": ["React Instantly", "Interrupt", "Dismiss Feelings", "Blame Others", "Angry Reply"]
        },
        "learning": {
            "good": ["Active Recall", "Spaced Repetition", "Practice", "Teach Others", "Ask Why"],
            "bad": ["Passive Reading", "Cram Last Night", "Copy Paste", "Memorize Only", "Skip Practice"]
        }
    }
    
    def __init__(self):
        """Initialize the item pool by building all items from themes"""
        self.all_items: List[Item] = self._build_item_pool()
    
    def _build_item_pool(self) -> List[Item]:
        """
        Build list of all items from themes
        
        Returns:
            List[Item]: List of 80 Item objects (40 good, 40 bad)
        """
        items = []
        
        for category, theme_items in self.ITEM_THEMES.items():
            # Add good items
            for text in theme_items["good"]:
                items.append(Item(text=text, is_good=True, category=category))
            
            # Add bad items
            for text in theme_items["bad"]:
                items.append(Item(text=text, is_good=False, category=category))
        
        return items
    
    def get_level_items(
        self,
        num_good: int,
        num_bad: int,
        preferred_themes: List[str] = None
    ) -> Tuple[List[Item], List[Item]]:
        """
        Get random items for a level
        
        Args:
            num_good (int): Number of good items to select
            num_bad (int): Number of bad items to select
            preferred_themes (List[str], optional): List of themes to prefer.
                If None, selects from all themes.
        
        Returns:
            Tuple[List[Item], List[Item]]: (good_items, bad_items)
        
        Example:
            >>> pool = ItemPool()
            >>> good, bad = pool.get_level_items(3, 2)
            >>> len(good), len(bad)
            (3, 2)
        """
        # Filter by type
        good_pool = [item for item in self.all_items if item.is_good]
        bad_pool = [item for item in self.all_items if not item.is_good]
        
        # Optional theme filtering
        if preferred_themes:
            good_pool = [i for i in good_pool if i.category in preferred_themes]
            bad_pool = [i for i in bad_pool if i.category in preferred_themes]
        
        # Random selection (no duplicates within a level)
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
            good_items (List[Item]): List of good items
            bad_items (List[Item]): List of bad items
        
        Returns:
            List[Item]: Shuffled list of all items
        
        Example:
            >>> good = [Item("Water", True, "healthy_habits")]
            >>> bad = [Item("Soda", False, "healthy_habits")]
            >>> shuffled = ItemPool.shuffle_display_items(good, bad)
            >>> len(shuffled)
            2
        """
        all_items = good_items + bad_items
        random.shuffle(all_items)
        return all_items
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about the item pool
        
        Returns:
            Dict[str, int]: Statistics including total, good, bad, and category counts
        """
        good_count = len([i for i in self.all_items if i.is_good])
        bad_count = len([i for i in self.all_items if not i.is_good])
        
        return {
            "total_items": len(self.all_items),
            "good_items": good_count,
            "bad_items": bad_count,
            "categories": len(self.ITEM_THEMES)
        }


class ItemDisplay:
    """
    Handles item display formatting
    
    Provides methods to format items for different display contexts:
    - Grid layout for memorization phase
    - Numbered list for recall phase
    """
    
    @staticmethod
    def format_grid(items: List[Item], columns: int = 3) -> str:
        """
        Format items in a grid layout
        
        Args:
            items (List[Item]): List of items to display
            columns (int): Number of columns (default 3)
        
        Returns:
            str: Formatted grid string with Rich markup
        
        Example:
            >>> items = [Item("Water", True, "healthy_habits")]
            >>> grid = ItemDisplay.format_grid(items)
            >>> "[green]" in grid
            True
        """
        lines = []
        
        for i in range(0, len(items), columns):
            row_items = items[i:i+columns]
            row_parts = []
            
            for item in row_items:
                symbol = "[+]" if item.is_good else "[-]"
                color = "green" if item.is_good else "red"
                row_parts.append(f"[{color}]{symbol}  {item.text:<20}[/{color}]")
            
            lines.append("  " + "  ".join(row_parts))
        
        return "\n".join(lines)
    
    @staticmethod
    def format_recall_list(items: List[Item]) -> str:
        """
        Format items as numbered list for recall phase
        
        Args:
            items (List[Item]): List of items to display
        
        Returns:
            str: Formatted numbered list (no symbols, just text)
        
        Example:
            >>> items = [Item("Water", True, "healthy_habits")]
            >>> recall_list = ItemDisplay.format_recall_list(items)
            >>> "1." in recall_list
            True
        """
        lines = []
        
        for i, item in enumerate(items, 1):
            lines.append(f"  {i}. {item.text:<30}")
        
        return "\n".join(lines)
    
    @staticmethod
    def create_display_box(content: str, title: str = "") -> str:
        """
        Create a bordered box for content
        
        Args:
            content (str): Content to display in box
            title (str): Optional title for the box
        
        Returns:
            str: Formatted box with borders
        """
        lines = content.split("\n")
        max_width = max(len(line) for line in lines) if lines else 0
        width = max(max_width, len(title)) + 4
        
        # Top border
        if title:
            box = f"+{'-' * (width - 2)}+\n"
            box += f"| {title.center(width - 4)} |\n"
            box += f"+{'-' * (width - 2)}+\n"
        else:
            box = f"+{'-' * (width - 2)}+\n"
        
        # Content
        for line in lines:
            box += f"| {line.ljust(width - 4)} |\n"
        
        # Bottom border
        box += f"+{'-' * (width - 2)}+\n"
        
        return box


# Module-level test function
def test_item_pool():
    """Test function to verify ItemPool functionality"""
    print("\n" + "=" * 60)
    print("  Item Pool Test Suite")
    print("=" * 60 + "\n")
    
    # Test 1: Item creation
    print("[OK] Test 1: Item Creation")
    item = Item("Water", True, "healthy_habits")
    assert item.text == "Water"
    assert item.is_good == True
    assert item.category == "healthy_habits"
    print(f"   Created item: {item}")
    print()
    
    # Test 2: ItemPool initialization
    print("[OK] Test 2: ItemPool Initialization")
    pool = ItemPool()
    stats = pool.get_stats()
    print(f"   Total items: {stats['total_items']}")
    print(f"   Good items: {stats['good_items']}")
    print(f"   Bad items: {stats['bad_items']}")
    print(f"   Categories: {stats['categories']}")
    assert stats['total_items'] == 80, f"Expected 80 items, got {stats['total_items']}"
    assert stats['good_items'] == 40, f"Expected 40 good items, got {stats['good_items']}"
    assert stats['bad_items'] == 40, f"Expected 40 bad items, got {stats['bad_items']}"
    assert stats['categories'] == 8, f"Expected 8 categories, got {stats['categories']}"
    print()
    
    # Test 3: Item selection
    print("[OK] Test 3: Item Selection")
    good, bad = pool.get_level_items(3, 2)
    print(f"   Selected {len(good)} good items:")
    for item in good:
        print(f"      - {item.text} ({item.category})")
    print(f"   Selected {len(bad)} bad items:")
    for item in bad:
        print(f"      - {item.text} ({item.category})")
    assert len(good) == 3, f"Expected 3 good items, got {len(good)}"
    assert len(bad) == 2, f"Expected 2 bad items, got {len(bad)}"
    assert all(i.is_good for i in good), "All good items should have is_good=True"
    assert all(not i.is_good for i in bad), "All bad items should have is_good=False"
    print()
    
    # Test 4: Shuffling
    print("[OK] Test 4: Item Shuffling")
    shuffled = ItemPool.shuffle_display_items(good, bad)
    print(f"   Shuffled {len(shuffled)} items")
    assert len(shuffled) == 5, f"Expected 5 items, got {len(shuffled)}"
    assert set(shuffled) == set(good + bad), "Shuffled items should match original items"
    print()
    
    # Test 5: Grid formatting
    print("[OK] Test 5: Grid Formatting")
    grid = ItemDisplay.format_grid(shuffled)
    print("   Grid layout:")
    print(grid)
    print()
    
    # Test 6: Recall list formatting
    print("[OK] Test 6: Recall List Formatting")
    recall_list = ItemDisplay.format_recall_list(shuffled)
    print("   Recall list:")
    print(recall_list)
    print()
    
    # Test 7: Theme filtering
    print("[OK] Test 7: Theme Filtering")
    good, bad = pool.get_level_items(2, 2, preferred_themes=["healthy_habits", "productivity"])
    print(f"   Selected items from specific themes:")
    for item in good + bad:
        print(f"      - {item.text} ({item.category})")
    assert all(i.category in ["healthy_habits", "productivity"] for i in good + bad)
    print()
    
    # Summary
    print("=" * 60)
    print("  SUCCESS: All Item Pool Tests Passed!")
    print("=" * 60 + "\n")
    
    print("Item Pool Statistics:")
    print(f"  - 8 thematic categories")
    print(f"  - 80 total items (40 good, 40 bad)")
    print(f"  - 10 items per category (5 good, 5 bad)")
    print()
    
    print("Categories:")
    for category in pool.ITEM_THEMES.keys():
        print(f"  - {category}")
    print()
    
    print("Ready for Story 1.3: Item Selection & Shuffling Logic!")
    print()


if __name__ == "__main__":
    # Run tests when module is executed directly
    test_item_pool()
