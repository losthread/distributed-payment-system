from ..core.redis import cache
import time

async def rate_limit(ip: str) -> bool:
  TOKEN_CAPACITY = 10
  REFILL_RATE = 1
  REFILL_INTERVAL = 1

  token_key = f"rate_limit:ip:{ip}:tokens"
  last_refill_key = f"rate_limit:ip:{ip}:last_refill"

  # Initialize token bucket
  await cache.set(token_key, TOKEN_CAPACITY, nx=True)
  await cache.set(last_refill_key, time.time(), nx=True)

  tokens = int(await cache.get(token_key))
  last_refill_time = float(await cache.get(last_refill_key))

  # Calculate completed refill intervals
  elapsed_time = time.time() - last_refill_time
  refills = int(elapsed_time // REFILL_INTERVAL)

  if refills > 0:
    tokens_to_add = refills * REFILL_RATE
    tokens = min(TOKEN_CAPACITY, tokens + tokens_to_add)

    last_refill_time += refills * REFILL_INTERVAL

    await cache.set(token_key, tokens)
    await cache.set(last_refill_key, last_refill_time)

  # Reject if no tokens
  if tokens < 1:
    return False

  # Consume one token
  await cache.decr(token_key)

  return True