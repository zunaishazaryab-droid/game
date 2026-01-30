"""
Views for Forget to Win browser-based game
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random

# Import game logic
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from item_pool import ItemPool
from game_engine import GameConfig, ScoreCalculator


def index(request):
    """Main game page"""
    return render(request, 'game/index.html')


def start_game(request):
    """Initialize a new game session"""
    # Clear any existing game state
    request.session['current_level'] = 1
    request.session['total_score'] = 0
    request.session['streak'] = 0
    request.session['level_history'] = []
    
    return JsonResponse({
        'success': True,
        'message': 'Game started!',
        'level': 1
    })


def get_level(request):
    """Get items for current level"""
    level = request.session.get('current_level', 1)
    
    # Get level configuration
    config = GameConfig.get_level_config(level)
    
    # Get items from pool
    good_items, bad_items = ItemPool.get_level_items(
        config['good_items'],
        config['bad_items']
    )
    
    # Shuffle for display
    all_items = ItemPool.shuffle_display_items(good_items, bad_items)
    
    # Store in session for validation
    request.session['good_items'] = [item.name for item in good_items]
    request.session['bad_items'] = [item.name for item in bad_items]
    request.session['all_items'] = [item.name for item in all_items]
    
    # Create display data with symbols
    display_items = [
        {
            'name': item.name,
            'symbol': '✅' if item.is_good else '❌',
            'is_good': item.is_good
        }
        for item in all_items
    ]
    
    return JsonResponse({
        'success': True,
        'level': level,
        'display_time': config['display_time'],
        'typing_time': GameConfig.TYPING_TIME.get(level, 30),
        'items': display_items,
        'total_items': len(all_items),
        'good_count': config['good_items'],
        'bad_count': config['bad_items']
    })


def get_recall_items(request):
    """Get items for recall phase (without symbols)"""
    all_items = request.session.get('all_items', [])
    
    # Shuffle again for recall (different order)
    random.shuffle(all_items)
    
    # Store shuffled order
    request.session['recall_order'] = all_items
    
    recall_items = [
        {
            'index': i,
            'name': name
        }
        for i, name in enumerate(all_items)
    ]
    
    return JsonResponse({
        'success': True,
        'items': recall_items
    })


@csrf_exempt
def submit_answer(request):
    """Validate user's answer and calculate score"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'})
    
    try:
        data = json.loads(request.body)
        selected_indices = data.get('selected', [])
        
        # Get stored data
        good_items = set(request.session.get('good_items', []))
        recall_order = request.session.get('recall_order', [])
        current_level = request.session.get('current_level', 1)
        current_streak = request.session.get('streak', 0)
        
        # Map indices to item names
        selected_items = set(recall_order[i] for i in selected_indices if i < len(recall_order))
        
        # Calculate results
        correct_good = len(selected_items & good_items)
        forgotten_good = len(good_items - selected_items)
        wrong_bad = len(selected_items - good_items)
        
        # Calculate score
        base_score = ScoreCalculator.calculate_base_score(
            correct_good,
            forgotten_good,
            wrong_bad
        )
        
        # Check if perfect (all good, no bad)
        is_perfect = (correct_good == len(good_items) and wrong_bad == 0)
        
        # Update streak
        if is_perfect:
            current_streak += 1
        else:
            current_streak = 0
        
        # Calculate streak bonus
        streak_bonus = ScoreCalculator.calculate_streak_bonus(base_score, current_streak)
        total_score = base_score + streak_bonus
        
        # Update session
        request.session['streak'] = current_streak
        cumulative_score = request.session.get('total_score', 0) + total_score
        request.session['total_score'] = cumulative_score
        
        # Store level history
        level_history = request.session.get('level_history', [])
        level_history.append({
            'level': current_level,
            'base_score': base_score,
            'streak_bonus': streak_bonus,
            'total_score': total_score,
            'correct': correct_good,
            'forgotten': forgotten_good,
            'wrong': wrong_bad,
            'is_perfect': is_perfect
        })
        request.session['level_history'] = level_history
        
        # Prepare response
        response_data = {
            'success': True,
            'correct_good': correct_good,
            'total_good': len(good_items),
            'forgotten_good': forgotten_good,
            'wrong_bad': wrong_bad,
            'base_score': base_score,
            'streak': current_streak,
            'streak_bonus': streak_bonus,
            'level_score': total_score,
            'cumulative_score': cumulative_score,
            'is_perfect': is_perfect,
            'good_items': list(good_items)
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def next_level(request):
    """Advance to next level"""
    current_level = request.session.get('current_level', 1)
    
    if current_level >= 5:
        # Game complete
        return JsonResponse({
            'success': True,
            'game_complete': True,
            'final_score': request.session.get('total_score', 0),
            'level_history': request.session.get('level_history', [])
        })
    
    # Advance level
    next_level_num = current_level + 1
    request.session['current_level'] = next_level_num
    
    return JsonResponse({
        'success': True,
        'game_complete': False,
        'next_level': next_level_num
    })


def get_final_results(request):
    """Get final game results"""
    total_score = request.session.get('total_score', 0)
    level_history = request.session.get('level_history', [])
    
    # Calculate rank
    max_score = GameConfig.get_max_possible_score()
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    rank_name, rank_badge, rank_tagline = GameConfig.get_rank(percentage)
    
    return JsonResponse({
        'success': True,
        'total_score': total_score,
        'max_score': max_score,
        'percentage': round(percentage, 1),
        'rank_name': rank_name,
        'rank_badge': rank_badge,
        'rank_tagline': rank_tagline,
        'level_history': level_history
    })
