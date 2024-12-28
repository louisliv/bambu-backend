# BambUI

> <span style="color:red;">This software is in a very early stage of development. Please note the liability clause of the AGPL license you agree to when using this program.</span>

A simple and slim UI for LAN mode of Bambu Lab Printers.
I do not trust Bambu Cloud and wanted an easy way to access my Printer P1S via home VPN.
I also do not like their Network Plugin for print monitoring, all current solutions including Home Assistant did not fit my needs, so I decided to build my own.
Currently, only P1S printers are supported. The UI shows a lot of buttons, but all disabled ones are not implemented yet.

Features:

- Add as many printers as you like
- Camera Stream
- UI control
- No Cloud required (works only in Lan Mode)
- Mobile friendly
- svelte, shadcn/ui, FastApi and docker (with vite and poetry)
- Connections running via server, so printer CPU is not overutilized
- Connect as many Clients as you want
- ready to use docker image (see `docker-compose.yaml`)

## Development

Create an `.env` based on `.env.example`
Set Up:

```bash
poetry install
uvicorn backend.main:app --port 8000 --env-file .env --reload
npm i
npm run dev
```

Lint

```bash
mypy .
ruff check .
ruff format .
npm run format
npm run build
```
