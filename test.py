import asyncio
from DB import connectDB
test = connectDB()
loop = asyncio.get_event_loop()
loop.run_until_complete(test.setting())
print(loop.run_until_complete(test.search("Gnar")))