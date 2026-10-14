# Day 1 - what blocks, what does not, and how to tell.
#
#   async def slow_lookup(seconds) -> str
#       await asyncio.sleep(seconds), then return f"waited {seconds}"
#
#   def blocking_lookup(seconds) -> str
#       time.sleep(seconds), then the same string. This is what a model call,
#       a database query or any ordinary library call looks like to asyncio.
#
#   async def run_all(delays) -> list[str]
#       slow_lookup for every delay, ALL AT ONCE, with asyncio.gather.
#       Results in the same order as `delays`.
#
#   async def run_blocking_wrong(delays) -> list[str]
#       call blocking_lookup for each delay, directly, inside this async
#       function. Write it - it is wrong on purpose, and the tests time it.
#
#   async def run_blocking_right(delays) -> list[str]
#       the same blocking calls, run at once: asyncio.to_thread(blocking_lookup, s)
#       for each, gathered.
#
#   def timed(coroutine) -> (result, seconds)
#       asyncio.run the coroutine, timing it with time.perf_counter
