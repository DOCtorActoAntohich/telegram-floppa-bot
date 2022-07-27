# Floppa Bot for Telegram

Inspired by [this Discord bot](https://github.com/htmlcsjs/CoffeeFloppa).

Simply put, I liked the above-mentioned bot and wanted to make something (a bit different) for myself, but in Telegram.

## How to run

It is assumed you already have the latest **Docker Compose V2** installed ([help](https://docs.docker.com/compose/)).

1. Clone the repository and `cd` to the root folder, where the `docker-compose.yml` is located.
2. Copy the contents of `sample.env` to the `.env` file (in the same directory).
3. Using any text editor, in the `.env` make changes as comments require.
4. Run `sudo docker compose up -d --build`
