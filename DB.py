import os, aiomysql, asyncio, json
from typing import Optional, Tuple
with open("riot.json") as json_file:
    champtbl = (json.load(json_file))[1]["champ"]

loop = asyncio.get_event_loop()
class connectDB:
    conn = None
    cur = None

    async def setting(self):
        self.conn = await aiomysql.connect(host=os.environ["DBHOST"], port=3306, user=os.environ["DBUSEID"],
                                    password=os.environ["DBKEY"], db="championdb", charset="utf8", autocommit=True, loop=loop)
        self.cur = await self.conn.cursor()

    async def insert(self, tbl: int, itemID: int) -> None:
        await self.cur.execute(query=f"INSERT items{tbl}(item) VALUES({itemID})")

    async def search(self, champName: str, itemID: Optional[int] = -1) -> Tuple[Tuple[int, int]]:
        if itemID == -1:
            await self.cur.execute(f"SELECT item, {champName} FROM items{champtbl[champName]} ORDER BY {champName} DESC;")
            return await self.cur.fetchall()
        else:
            await self.cur.execute(query=f"SELECT {champName} FROM items{champtbl[champName]} WHERE item = {itemID};")
            return await self.cur.fetchall()[0][0]
    
    async def update(self, champName: str, itemID: int, num: Optional[int] = 1) -> None:
        value = await self.search(champName, itemID)
        await self.cur.execute(query=f"UPDATE items{champtbl[champName]} SET {champName} = {value + num} WHERE item = {itemID};")