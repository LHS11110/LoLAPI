from typing import List, Dict
from fastapi import FastAPI
import uvicorn, asyncio
from LoLHttpsClient import LolHttpsClient
app = FastAPI()
lol = LolHttpsClient()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/renewal/match/{summonerName}")
async def summoner_match(summonerName: str, start: int, count: int) -> List[Dict[str, str]]:
    match_list = []
    for match_id in await lol.match_v5_by_puuid((await lol.summoner_v4_by_name(summonerName))["puuid"], start, count):
        match_list.append(lol.match_v5_matchs(match_id))
    match_list = await asyncio.gather(*match_list)
    return match_list

@app.get("/search/profile/{summonerName}")
async def summoner_profile(summonerName: str) -> Dict[str, str]:
    summoner_profile_info = await lol.league_v4_by_summoner((await lol.summoner_v4_by_name(summonerName))["id"])
    return summoner_profile_info

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8099, reload=True, workers=4)