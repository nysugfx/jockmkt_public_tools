import pandas as pd
from jockmkt_sdk.client import Client
import time
from datetime import datetime

secret_key = "<INSERT SECRET KEY HERE>"  # e.g. "xxx"
api_key = "<INSERT API KEY HERE>"  # e.g. "jm_key_xxx"

client = Client(secret_key, api_key)

path_to_csv = "INSERT FILE PATH HERE"  # e.g. (mac) "/Users/yourname/Downloads/jockmkt-mlb-evt_62d77dc4bd5455620a56e14c439a2b5e-1658496145658.csv"

sleep = False  # ADJUST THIS IF YOU DO NOT WANT THE SCRIPT TO AUTOMATICALLY SLEEP FOR YOU

def read_jm_csv(filepath):
    """
    Read in your file to pandas
    """
    return pd.read_csv(filepath)

def handle_csv(file):
    """
    Drop all players for which we have no prices or quantities
    """
    if 'price' not in file.columns:
        raise KeyError("Could not find your prices! ensure that you titled the column 'price'!")
    if 'quantity' not in file.columns:
        raise KeyError("Could not find your prices! ensure that you titled the column 'quantity'!")

    return file.dropna(subset=['price', 'quantity'])

csv = handle_csv(read_jm_csv(path_to_csv))

def get_event():
    """
    Get event information using the event_id in the filename
    """
    print("getting event")
    event_id = path_to_csv.split("-")[2]
    return client.get_event(event_id)

event_info = get_event()

def join_event(event):
    """
    Join event (if the user has not already joined)
    """
    print('joining event')
    try:
        client.create_entry(event.event_id)
    except:
        print('event already joined')

join_event(event_info)

def get_sleeptime(event, parsed_csv):
    """
    Calculate a sleep time based on how many orders need to be placed, so the user can place orders as late in IPO phase possible.
    """
    num_orders = len(parsed_csv)
    time_required_to_place = ((num_orders / 10) * 60) + 135
    ipo_end = (event.ipo_end) / 1000
    now = round(time.time(), 0)

    sleeptime = ipo_end - now - time_required_to_place

    sleep_til_ts = ipo_end - time_required_to_place

    sleep_til_dt = datetime.fromtimestamp(sleep_til_ts).strftime("%Y-%m-%d %H:%M:%S")

    if sleep:
        print(f'Sleeping until {sleep_til_dt}!')
        time.sleep(sleeptime)


get_sleeptime(event_info, csv)

def fetch_open_orders(event):
    """
    Fetch all open orders so we don't place orders on the same player twice
    """
    open_orders = [i.tradeable_id for i in client.get_orders(event_id=event.event_id, active=True)]
    return open_orders

def fetch_prices():
    """
    Build a dictionary with the last price so we don't bid on players whose price is higher than ours
    """
    event = get_event()
    price_dict = dict((i.tradeable_id, i.last or 1) for i in event.tradeables)
    return price_dict

def place_orders(parsed_csv):
    """
    Fetch open orders
    Fetch prices
    If player doesn't have an open order and our bid is higher than the current high bid, place an order

    Prints a list of players for which there were
    """
    errors = []
    open_orders = fetch_open_orders(event_info)
    for key, value in parsed_csv.iterrows():
        current_bid = fetch_prices()
        price = round(value['price'], 2)
        quantity = round(value['quantity'], 0)
        tradeable_id = value['TRADEABLE_ID']
        name = value['NAME']
        try:
            if tradeable_id not in open_orders and price > current_bid[tradeable_id]:
                client.place_order(tradeable_id, price, side = 'buy', phase = 'ipo', qty=quantity)
            elif tradeable_id in open_orders:
                print("you've already placed an order on this guy!")
            elif price <= current_bid[tradeable_id]:
                print('your bid is lower than the current price.')
        except:
            errors.append(f'{name}: price: {price}, quantity: {quantity}')
            print(f'could not place an order on {name}. Place this order manually!')

    if len(errors) == 0:
        print('no errors!')
        return
    else:
        print("\nERRORS: please place the orders below manually\n")
        print([f'{error} \n' for error in errors])

place_orders(csv)
