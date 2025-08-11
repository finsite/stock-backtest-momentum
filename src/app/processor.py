"""Processor module for stock-backtest-momentum signal generation.

Validates input messages and computes a momentum signal using
price change over time or momentum indicators.
"""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import ValidatedMessage
from app.utils.validate_data import validate_message_schema

logger = setup_logger(__name__)


def validate_input_message(message: dict[str, Any]) -> ValidatedMessage:
    """Validate the incoming raw message against the expected schema.

    Args:
        message (dict[str, Any]): Raw input message.

    Returns:
        ValidatedMessage: A validated message object.

    Raises:
        ValueError: If the input format is invalid.

    """
    logger.debug("🔍 Validating message schema...")
    if not validate_message_schema(message):
        logger.error("❌ Invalid message schema: %s", message)
        raise ValueError("Invalid message format")
    return message  # type: ignore[return-value]


def compute_momentum_signal(message: ValidatedMessage) -> dict[str, Any]:
    """Compute a momentum signal using recent price change.

    Args:
        message (ValidatedMessage): The validated input data.

    Returns:
        dict[str, Any]: Enriched message with momentum signal and metric.

    """
    symbol = message.get("symbol", "UNKNOWN")
    price = float(message.get("price", 100.0))
    price_lookback = float(message.get("price_lookback", 95.0))  # Price N periods ago

    logger.info("⚡ Computing momentum signal for %s", symbol)

    momentum = (price - price_lookback) / price_lookback
    signal = "BUY" if momentum > 0.05 else "SELL" if momentum < -0.05 else "HOLD"

    result = {
        "momentum_value": round(momentum, 4),
        "momentum_signal": signal,
    }

    logger.debug("📈 Momentum result for %s: %s", symbol, result)
    return {**message, **result}
