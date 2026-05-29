# Copyright (c) 2026 iiPython
# Stockfuck - Multiplayer stock market game thing

# Modules
import json
import asyncio
import math
from random import randint, choice
from pathlib import Path

from websockets.asyncio.server import ServerConnection, serve

# Initialize rich
from rich.console import Console
from rich.traceback import install

install()  # Setup nice-looking tracebacks

RICH_CONSOLE = Console()

# Configuration
GAME_MONTH     = randint(5, 7)
GAME_LENGTH    = 10
GAME_YEAR      = 2000 + randint(30, 50)
GAME_START_DAY = randint(1, 28 - GAME_LENGTH)
GAME_EVENT_MIN = 0
GAME_EVENT_MAX = 2

# Data handlers
DATA_FOLDER  = Path(__file__).parent / "data"
GAME_EVENTS  = json.loads((DATA_FOLDER / "events.json").read_text())
GAME_TICKERS = json.loads((DATA_FOLDER / "tickers.json").read_text())

# Game logic
class Player:
    def __init__(self, websocket: ServerConnection, market: "Stocks") -> None:
        self.market = market
        self.websocket = websocket

        # Starting cash
        self.cash = 5000

        # Initialize share count
        self.shares = {ticker: 0 for ticker in GAME_TICKERS}

    def purchase_shares(self, ticker: str, amount: int) -> None:
        max_shares = math.floor(self.cash / self.market.stock_prices[ticker])
        if amount > max_shares:
            amount = max_shares

        self.cash -= self.market.stock_prices[ticker] * amount
        self.shares[ticker] += amount

    def sell_shares(self, ticker: str, amount: int) -> None:
        if amount > self.shares[ticker]:
            amount = self.shares[ticker]

        self.cash += self.market.stock_prices[ticker] * amount
        self.shares[ticker] -= amount

class Stocks:
    def __init__(self) -> None:
        self.game_date = 0

        # Initial stock prices
        self.stock_prices = {
            ticker: randint(5, 400) + (randint(1, 100) / 100)
            for ticker in GAME_TICKERS
        }

        # Individual per-ticker share price changes
        self.price_history = {ticker: [] for ticker in GAME_TICKERS}

        # Preload the tickers
        asyncio.create_task(self.preload())

    def normalize(self) -> None:
        for ticker, price in self.stock_prices.items():
            self.stock_prices[ticker] = round(price, 2)

    async def preload(self) -> None:
        for _ in range(10):
            await self.step(preloading = True)

        while not await asyncio.sleep(5):
            await self.step()

    async def step(self, preloading: bool = False) -> None:

        # Apply a random amount of general market change
        for ticker in self.stock_prices:
            old_price = self.stock_prices[ticker]
            change = randint(-20, 20)
            self.stock_prices[ticker] *= 1 + (change / 100)
            print(f"{ticker} ({GAME_TICKERS[ticker]}) just went from ${old_price:.2f} to ${self.stock_prices[ticker]:.2f} [{'red' if change < 0 else 'green'}]({change:+}%)")

        # Afterwards, apply events
        event_count, events_used = randint(GAME_EVENT_MIN, GAME_EVENT_MAX), []
        while len(events_used) != event_count:
            chosen_event = choice(list(GAME_EVENTS.keys()))
            if chosen_event in events_used:
                continue

            events_used.append(chosen_event)
            for ticker, adjustment in GAME_EVENTS[chosen_event]["tick"].items():
                self.stock_prices[ticker] *= 1 + adjustment

            print(f"[Emit] Event = {chosen_event}")

        # Normalize ticker prices
        self.normalize()

        # Save ticker prices
        for ticker, price in self.stock_prices.items():

            # Add current ticker price, keep 10 most recent prices
            self.price_history[ticker] = ([price] + self.price_history[ticker])[:10]

        # Lastly, update the date
        if not preloading:
            self.game_date += 1

            # Show terminal summary
            RICH_CONSOLE.clear()
            RICH_CONSOLE.rule(f"Stockfuck - 0{GAME_MONTH}/{GAME_START_DAY + self.game_date:02d}/{GAME_YEAR} (Day {self.game_date})")

            for ticker, price_history in self.price_history.items():
                new_price, old_price = price_history[:2]
                price_change = round(((new_price / old_price) - 1) * 100)
                RICH_CONSOLE.print(f"{ticker}: ${old_price:6.2f} -> ${new_price:6.2f} [{'red' if price_change < 0 else 'green'}]({price_change:+3}%)")

    # Websocket control
    async def handle_websocket(self, websocket: ServerConnection) -> None:
        async for message in websocket:
            print(message)

# Launch websocket handling
async def main():
    await (await serve(Stocks().handle_websocket, "localhost", 8765)).serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
