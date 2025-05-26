from fastapi import FastAPI, Query
import requests

app = FastAPI()


API_KEY = "9JUHtZRMb7JQFWzmpPPsQgCuWaNhL0zT5inGt0LLgzsT7T8M0ycKxfs9nZlOfg2a"

def get_token_info_aveapi(keyword: str):
    url = f"https://prod.ave-api.com/v2/tokens?keyword={keyword}"

    headers = {"X-API-KEY": API_KEY}

    try:
        # resp
        response = requests.get(url, headers=headers) 
        response.raise_for_status()

        # get data
        tokens = response.json().get("data", [])

        # 401 404 ...
        if not tokens:
            return {"error": "No token found."}
        # first token
        token = tokens[0]
        return {
            "symbol": token.get("symbol"),
            "CA": token.get("token"),
            "Max_Supply": token.get("total"),
            "MC": token.get("market_cap"),
            "FDV": token.get("fdv"),
        }
    # ERROR CHECK 
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except Exception as e:
        return {"error": f"error(other than HTTP & API request): {e}"}


@app.get("/api/v1/get_token_info")
def api_get_token_info(keyword: str = Query(..., min_length=1)):

    return get_token_info_aveapi(keyword)