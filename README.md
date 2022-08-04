# Floppa Bot for Telegram

Inspired by [this Discord bot](https://github.com/htmlcsjs/CoffeeFloppa).

Simply put, I liked the above-mentioned bot and wanted to make something (a bit different) for myself, but in Telegram.

## How to run

It is assumed you already have the latest **Docker Compose V2** installed ([help](https://docs.docker.com/compose/)).

1. Clone the repository and `cd` to the root folder, where the `docker-compose.yml` is located.
2. Copy the contents of `sample.env` to the `.env` file (in the same directory).
3. Using any text editor, in the `.env` make changes as comments require.
4. Run `sudo docker compose up -d --build`

## Extras

*In the art of programming, you trade off between readability and performance*

Previous version of the project (which hides in private repository) was poorly made and barely worked.
The code was messy and had a relatively high coupling. Additionally, it was running Redis,
which is cool and simple, but I realized I like MongoDB more (even though it doesn't like me).

Thus, the current project has slightly different goals. While it is just a re-implementation of the same bot
but with MongoDB and Pydantic, this project tries to follow *The Clean Architecture*
and also implements some unit-tests.

However, this design is overkill.
The bot turned out to be intentionally over-engineered, but my goals were reached.
