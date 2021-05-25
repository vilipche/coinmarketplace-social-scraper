Python script that scrapes data from coinmarketplace.
Specifiaclly scrapes the twitter profiles of each crypt currency sorted by the marketcap. 

## How to install

```
# clone the repo
$ git clone https://github.com/vilipche/coinmarketplace-social-scraper.git

# change the directory
$ cd coinmarketplace-social-scraper

# install requirements
$ python3 -m pip install -r requirements.txt
```

## Use --help

```
$ python3 main.py --help
usage: main.py [-h] [-f FILENAME] [-q] n [begin_from]

Scrape and store data

positional arguments:
  n                     display a square of a given number
  begin_from            Select from which position to begin

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Name the file of the .csv
  -q, --quiet

```

## Example

```
$ python3 main.py 10 1
  1 BTC bitcoin 702,918,781,666
  2 ETH ethereum 286,854,137,946 @ethereum
  3 USDT tether 58,607,992,313 @Tether_to
  4 BNB binance-coin 52,050,182,383 @binance
  5 ADA cardano 50,897,730,279 @Cardano
  6 XRP xrp 48,477,472,994 @Ripple
  7 DOGE dogecoin 47,166,791,427 @dogecoin
  8 DOT polkadot-new 22,872,752,659 @Polkadot
  9 ICP internet-computer 18,356,269,851 @dfinity
  10 USDC usd-coin 14,386,880,576
  Saved to crypto-social.csv
```

### Feel free to contribute :)
