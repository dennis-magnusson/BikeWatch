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

## Disclaimer

This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

Users are responsible for ensuring their use of this software complies with the terms of service of any websites they scrape.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
