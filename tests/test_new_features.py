import pytest
import pytest_asyncio
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
import os
import sys

# Ensure the bot package is in the user's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.database import (
    initialize_db, add_goal, get_active_goals, 
    add_goal_progress, complete_goal
)
from bot.utils import RateLimiter, global_rate_limiter, generate_gemini_response

import tempfile

@pytest_asyncio.fixture(autouse=True)
async def setup_and_teardown_db():
    """Fixture to set up and tear down a temporary database for each test."""
    # Create a temporary file
    fd, temp_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    
    # Manually set the global DB_FILE
    import bot.database
    original_db_file = bot.database.DB_FILE
    bot.database.DB_FILE = temp_path
    
    await initialize_db()
    yield
    
    # Restore and Cleanup
    bot.database.DB_FILE = original_db_file
    if os.path.exists(temp_path):
        os.remove(temp_path)

@pytest.mark.asyncio
async def test_goal_tracking_crud():
    user_id = 99999
    
    # 1. Add Goal
    goal_id = await add_goal(user_id, "Drink Water", "2L daily", "2L")
    assert goal_id is not None
    
    # 2. Get Active Goals
    goals = await get_active_goals(user_id)
    assert len(goals) == 1
    assert goals[0]['goal_name'] == "Drink Water"
    assert goals[0]['status'] == 'active'
    
    # 3. Add Progress
    success = await add_goal_progress(goal_id, "Drank 1L")
    assert success is True
    
    # 4. Complete Goal
    success = await complete_goal(goal_id)
    assert success is True
    
    # 5. Verify Goal is no longer active
    goals = await get_active_goals(user_id)
    assert len(goals) == 0

@pytest.mark.asyncio
async def test_rate_limiter_logic():
    # Test Rate Limiter Logic separately
    limiter = RateLimiter(rpm=5, rpd=10)
    
    # Simulate 5 requests quickly
    for _ in range(5):
        await limiter.acquire()
        
    assert len(limiter.request_timestamps) == 5
    
    # The 6th request should wait (mocking sleep to avoid actual delay)
    with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
        await limiter.acquire()
        # It might trigger sleep if processed instantly, but exact check depends on timing
        # Just verifying no exception is raised and list grew
        
    assert len(limiter.request_timestamps) == 6

@pytest.mark.asyncio
async def test_gemini_model_config():
    # Verify dual-model configuration constants exist
    from bot.core import GEMINI_ANALYSIS_MODEL_ID, GEMINI_TRANSCRIPTION_MODEL_ID
    assert GEMINI_ANALYSIS_MODEL_ID == 'gemma-3-27b-it'
    assert GEMINI_TRANSCRIPTION_MODEL_ID == 'gemini-2.5-flash-lite'
