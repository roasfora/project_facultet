import requests
import pandas as pd


def fetch_eth_market_data(vs_currency="usd", days=1):
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def save_eth_data_to_csv(data, filename="ethereum_data.csv"):
    prices = data.get("prices", [])
    market_caps = data.get("market_caps", [])
    total_volumes = data.get("total_volumes", [])

    rows = []
    for i in range(len(prices)):
        price_time, price_value = prices[i]
        market_cap_value = market_caps[i][1] if i < len(market_caps) else None
        total_volume_value = total_volumes[i][1] if i < len(total_volumes) else None
        rows.append(
            {
                "timestamp_ms": price_time,
                "price": price_value,
                "market_cap": market_cap_value,
                "total_volume": total_volume_value,
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)
    return filename


def main():
    print("Fetching Ethereum market data from CoinGecko...")
    data = fetch_eth_market_data(vs_currency="usd", days=1)
    output_file = save_eth_data_to_csv(data, filename="ethereum_data.csv")
    print(f"Saved Ethereum data to {output_file}")


if __name__ == "__main__":
    main()
