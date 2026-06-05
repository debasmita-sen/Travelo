"""Tests for thin tool wrappers that the orchestrator and agents use.

These ensure that the project tools return shaped outputs (budget status,
attractions list) suitable for downstream assembly into itineraries.
"""

from tools.budget_tools import calculate_budget
from tools.attraction_tools import search_attractions


def test_budget_tool_status():
    result = calculate_budget("Paris", 2, 1, 1000)
    assert result["status"] in {"comfortable", "tight"}


def test_attraction_tool_returns_items():
    assert search_attractions("Tokyo", "art")
