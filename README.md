# BikeWatch

BikeWatch is service that monitors used bike listings on fillaritori.com and sends alerts to users via Telegram according to their selected search filters. 

# Features
-   Register filters with a Telegram bot to receive personalized notifications matching your filters
-   Browse all listings scraped from source websites and filter them by price, location, category and size
-   Register filters with a Telegram bot to receive personalized notifications matching your filters

## Demo

### Frontend

<p float="left">
<img src="docs/assets/frontend.png" width="600" />
</p>

### Telegram Bot

<p float="left">
<img src="docs/assets/notification.png" width="220" />
<img src="docs/assets/bot_start.gif" width="220" />
<img src="docs/assets/bot_help.gif" width="220" />
</p>

## Getting started

-   Run the services using docker-compose:

`docker compose -f docker/docker-compose.yaml up --build`

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
