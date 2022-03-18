from typing import List, Dict, Optional
from fastapi import FastAPI
from LoLHttpsClient import LolHttpsClient
import uvicorn, asyncio, pymysql
app = FastAPI()
lol = LolHttpsClient()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/search/summonerinfo/{summonerName}")
async def summonerinfo(summonerName: str) -> Dict[str, str]:
    return await lol.summoner_v4_by_name(summonerName)

@app.get("/renewal/match/{summonerpuuid}")
async def summoner_match(summonerpuuid: str, start: Optional[int] = 0, count: Optional[int] = 20) -> List[Dict[str, str]]:
    match_list = []
    for match_id in await lol.match_v5_by_puuid(summonerpuuid, start, count):
        match_list.append(lol.match_v5_matchs(match_id))
    match_list = await asyncio.gather(*match_list)
    info = []
    for _ in match_list:
        info.append(lol.summoner_match_info(_["info"]))
    return await asyncio.gather(*info)

@app.get("/search/profile/{summonerid}")
async def summoner_profile(summonerid: str) -> List[Dict[str, str]]:
    return await lol.league_v4_by_summoner(summonerid)

@app.get("/freeChampion")
async def free_champion() -> Dict[str, str]:
    return await lol.champion_v4_free_champion()

@app.get("/championmastery/{summonerid}")
async def get_championmastery(summonerid: str, count: Optional[int] = 7) -> List[Dict[str, str]]:
    return (await lol.champion_mastery_v4(summonerid))[:count]

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8099, reload=True, workers=4)
