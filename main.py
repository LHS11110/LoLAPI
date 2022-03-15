from typing import Optional
from fastapi import FastAPI
import uvicorn, aiohttp, json
app = FastAPI()
with open("riot_header_Info.json") as json_file:
    riot_header = json.load(json_file)

async def summoner_v4_by_name(summonerName):
    async with aiohttp.ClientSession(headers=riot_header) as session:
        async with session.get(f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}') as response:
            html = await response.text()
    return json.loads(html)["puuid"]

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/search/{summonerName}")
async def summoner_search(summonerName: str):
    summonerInfo: str = await summoner_v4_by_name(summonerName)
    return {"summonerpuuid": summonerInfo}

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8099, reload=True, workers=4)