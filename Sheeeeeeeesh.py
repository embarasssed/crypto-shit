import json
import asyncio
import websockets
import requests

# Метод для обработки полученных данных о стакане (order book)
def process_order_book(pair, data):
    # Здесь вы можете обработать данные стакана по своему усмотрению
    print(f"Pair: {pair}, Data: {data}")

# Асинхронная функция для подключения к WebSocket для указанной пары
async def connect_to_websocket(pair):
    ws_url = f"wss://stream.binance.com:9443/ws/{pair.lower()}@depth"

    async with websockets.connect(ws_url) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data.get("e") == "depthUpdate":
                process_order_book(pair, data)

# Метод для получения списка пар изолированной маржи доступных для торговли на Binance
def get_isolated_margin_pairs():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        isolated_margin_pairs = [symbol["symbol"] for symbol in data["symbols"] if symbol.get("isMarginTradingAllowed", False) and symbol.get("quoteAsset", "") == "USDT"]
        return isolated_margin_pairs

# Асинхронная функция для подключения ко всем парам
async def main():
    isolated_margin_pairs = get_isolated_margin_pairs()
    tasks = [connect_to_websocket(pair) for pair in isolated_margin_pairs]
    await asyncio.gather(*tasks)

# Запускаем асинхронную функцию
asyncio.run(main())
