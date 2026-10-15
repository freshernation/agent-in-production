# Start from your week-05/milestone/config.py, and add two settings.
#
#   fallback_provider   FALLBACK_PROVIDER, default "" (no fallback)
#   daily_budget        DAILY_BUDGET as a float, default 1.0, must be above 0
#
# Refuse to start (ValueError) when FALLBACK_PROVIDER is the same as
# AGENT_PROVIDER: when one is down, so is the other.
#
# Add both to redacted() - neither is a secret.
