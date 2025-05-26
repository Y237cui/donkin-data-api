from fastapi import FastAPI, Query
import requests

app = FastAPI()

API_KEY = "9JUHtZRMb7JQFWzmpPPsQgCuWaNhL0zT5inGt0LLgzsT7T8M0ycKxfs9nZlOfg2a"

# the same as get_token_info
def get_token_info_aveapi(keyword: str):
    url = f"https://prod.ave-api.com/v2/tokens?keyword={keyword}"
    headers = {"X-API-KEY": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tokens = response.json().get("data", [])
        if not tokens:
            return None, {"error": "No token found."}

        token = tokens[0]
        return {
            "symbol": token.get("symbol"),
            "CA": token.get("token"),
            "Chain": token.get("chain"), # chain here
            "Max_Supply": float(token.get("total", 0)),
            "MC": token.get("market_cap"),
            "FDV": token.get("fdv"),
        }, None

    except Exception as e:
        return None, {"error": f"Error fetching token info: {e}"}


def get_top_holders(token_id: str):
    url = f"https://prod.ave-api.com/v2/tokens/top100/{token_id}"
    headers = {"X-API-KEY": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        raw = response.json()
        data = raw.get("data")

        holders = []

        # format1: data is dict， holders
        if isinstance(data, dict) and "holders" in data:
            holders = data["holders"]
            for h in holders:
                h["amount"] = h.get("amount", 0)
        # f2: data is list, list of holders
        elif isinstance(data, list):
            holders = [
                {
                    "address": h.get("address"),
                    "amount": h.get("amount_cur", 0),
                    # if later api fixed
                    # "amount_diff_3days": h.get("amount_diff_3days", 0)
                    
                }
                for h in data
            ]
        else:
            return None, {"error": "Unrecognized holder data format"}

        if not holders:
            return None, {"error": "Holder list is empty"}

        return holders, None

    except Exception as e:
        return None, {"error": f"Error fetching top holders: {e}"}


@app.get("/api/v1/get_token_info")

def api_get_token_info(keyword: str = Query(..., min_length=1)):
    token_info, error = get_token_info_aveapi(keyword)
    if error:
        return error
    
    # get supply, ca ,chain
    max_supply = token_info.get("Max_Supply", 0)
    ca = token_info.get("CA")
    chain = token_info.get("Chain")
    if not max_supply or not ca or not chain:
        return {"error": "Missing required token info"}

    token_id = f"{ca}-{chain}"
    holders, holder_err = get_top_holders(token_id)
    # error status
    if holder_err:
        token_info.update({
            "Top10_Percent": "N/A",
            "Top100_Percent": "N/A",
            "Top10_Holders": [],
            "Top100_Holders": [],
            "holder_calc_error": holder_err.get("error")
        })
        return token_info

    try:
        # sort by amount
        holders_sorted = sorted(holders, key=lambda h: h.get("amount", 0), reverse=True)
        top10 = holders_sorted[:10]
        top100 = holders_sorted[:100]

        top10_total = sum(h["amount"] for h in top10)
        top100_total = sum(h["amount"] for h in top100)

        token_info["Top10_Percent"] = f"{top10_total / max_supply * 100}%"
        token_info["Top100_Percent"] = f"{top100_total / max_supply * 100}%"

        token_info["Top10_Holders"] = [
            {
                "rank": i + 1,
                "address": h.get("address"),
                "percent": f"{h['amount'] / max_supply * 100}%"
            }
            for i, h in enumerate(top10)
        ]

        token_info["Top100_Holders"] = [
            {
                "rank": i + 1,
                "address": h.get("address"),
                "percent": f"{h['amount'] / max_supply * 100}%"
            }
            for i, h in enumerate(top100)
        ]

    except Exception as e:
        token_info.update({
            "Top10_Percent": "N/A",
            "Top100_Percent": "N/A",
            "Top10_Holders": [],
            "Top100_Holders": [],
            "holder_calc_error": str(e)
        })

    return token_info