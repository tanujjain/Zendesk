import pytest

# Before running the tests:
# 1. Go to root of the project directory
# 2. Make sure opik server is running on port 5173
# 3. Run the following command: export OPIK_URL_OVERRIDE="http://localhost:5173/"
# 4. Run tests: pytest tests/test_evaluation.py

from components.evaluation import EvaluateAppropriateness

eval_appropriateness = EvaluateAppropriateness()

@pytest.mark.asyncio
async def test_eval_succeeds_inappropriate():
    conversation_history = [{"role": "assistant", "content": "How can I help you today?"},
                            {"role": "user", "content": "Please cancel orders 34978 and 11334"},
                            {"role": "assistant",
                             "content": "Sorry, the order contains Perishable items. As per Policy, it can't be cancelled."},
                            {"role": "user", "content": "what? perishable?"},
                            {"role": "assistant",
                             "content": "Your order status is Pending. Can I help you with anything else?"},
                            {"role": "user", "content": "which order are you talking about?"},
                            {"role": "assistant",
                             "content": "Your order status is Pending. Can I help you with anything else?"}
                            ]
    response = await eval_appropriateness(conversation_history)
    assert response == "Inappropriate"


@pytest.mark.asyncio
async def test_eval_succeeds_appropriate():
    conversation_history = [{"role": "assistant", "content": "How can I help you today?"},
                            {"role": "user", "content": "i placed an order long ago and still haven't got it"},
                            {"role": "assistant", "content": "Sorry, I could not find the order number. Please provide the order number."},
                            {"role": "user", "content": "54678"},
                            {"role": "assistant", "content": "Your order status is Pending. Can I help you with anything else?"}
                            ]
    response = await eval_appropriateness(conversation_history)
    assert response == "Appropriate"