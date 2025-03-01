# BikeWatch

BikeWatch is service that monitors forum websites, where people resell old bikes (eg. fillaritori). Users of the service can easily view the offerings and set notifications for themselves for certain listings that they are interested in. Users will then be notified of new bikes that they are interested in via a Telegram bot.

## Features

-   Browse all listings scraped from source websites and filter them by price, location, category and size
-   Register filters with a Telegram bot to receive personalized notifications matching your filters

## Demo

<p float="left">
<img src="docs/assets/notification-portrait.png" width="220" />
</p>

## Getting started

-   Run the services using docker-compose:

`docker compose -f docker/docker-compose.yaml up --build`

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
