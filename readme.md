# api function: .py for several use

# how to run
change resp(uvicorn) in run_api.sh
## code
./run_app.sh
## website
http://localhost:8000/docs

### get_token_info: 
        return {
            "symbol",
            "CA",
            "Max_Supply",
            "MC",
            "FDV",
        }

### get_top:
        return {
            "symbol",
            "CA",
            "Chain",
            "Max_Supply",
            "MC",
            "FDV",
            "Top10_Percent",
            "Top100_Percent",
            "Top10_Holders":[list of {"rank",
                                      "address",
                                      "percent"
                                }
                            ]
            "Top100_Holders":[list of {"rank",
                                      "address",
                                      "percent"
                                }
                            ]            

