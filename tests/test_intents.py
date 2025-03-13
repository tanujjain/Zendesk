import pytest

# Before running the tests:
# 1. Go to root of the project directory
# 2. Make sure opik server is running on port 5173
# 3. Run the following command: export OPIK_URL_OVERRIDE="http://localhost:5173/"
# 4. Run tests: pytest tests/test_intents.py

from components.next_action_classification import GetNextStep

next_action = GetNextStep()

@pytest.mark.asyncio
async def test_cancellation_succeeds():
    conversation_history = [{"role": "assistant", "content": "How can I help you today?"},
                            {"role": "user", "content": "Please cancel order 11334"}]
    response = await next_action(conversation_history)
    assert response == "cancel_order"


@pytest.mark.asyncio
async def test_tracking_succeeds():
    conversation_history = [{"role": "assistant", "content": "How can I help you today?"},
                            {"role": "user", "content": "i placed an order long ago and still haven't got it"},
                            {"role": "assistant", "content": "Sorry, I could not find the order number. Please provide the order number."},
                            {"role": "user", "content": "54678"}]
    response = await next_action(conversation_history)
    assert response == "track_order"


@pytest.mark.asyncio
async def test_other_succeeds():
    conversation_history = [{"role": "assistant", "content": "How can I help you today?"},
                            {"role": "user", "content": "hello"}]
    response = await next_action(conversation_history)
    assert response == "Other"


@pytest.mark.asyncio
async def test_end_conversation_succeeds():
    conversation_history = [{"role": "assistant", "content": "How can I help you today?"},
                            {"role": "user", "content": "i placed an order long ago and still haven't got it"},
                            {"role": "assistant", "content": "Sorry, I could not find the order number. Please provide the order number."},
                            {"role": "user", "content": "54678"},
                            {"role": "assistant", "content": "Your order status is Pending. Can I help you with anything else?"},
                            {"role": "user", "content": "no, thanks"}]
    response = await next_action(conversation_history)
    assert response == "end_conversation"