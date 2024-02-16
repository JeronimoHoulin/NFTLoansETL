import requests
import json

url = "https://api.mainnet-beta.solana.com"

# Set the headers
headers = {
    "Content-Type": "application/json"
}


#Test loans:
loan1 = '5Te39C5cvQvKPssueQDwsw1RKFCD5o79oXK3jHb5wjbogV82aEe8dsyxNUmeL4LJePZ1CgcoGdLhY9gRcQvwFn4K'
loan2 = 'iJgWtWTxvwJ1hkKLpcoCDLbVJDdiTm9xjwYXY68ydYsyhogFgYt97z422uZDxphCHfioLotQhYvXMAGx14mSwsS'
loan3 = '43X5ejZaXrMBUnDrCr6SjX9x2pBsUcPRnvqASJpxA7y76htwV6hS5EMvYrPcR7ZraMcYw2eRZf4SX5vmr9d85BoW' #Ovol loan

#Test Foreclosed loans:
close1 = '4GoW7WjbY7etuREfJxrZmr9fmSfMXkRmNNwiYCMSYA93m9ove7hSTQHJGZB8vt2DL8AeSHKnYPYFkqtsdaJo8KH5'
close2 = '3hNTkB9TwmteEu4VJVefxVJPDS9BA5WjzwNB4fkA65quLnLdxg4QtNpEgixrFkK8dnCfgewxWebckfbxYXDJyc94'

#Test Rescind loan:
rescind1 = '4VNJzgHiAKL1Rb77BeK4Y55ao33ncrXye63Zcq8rtUdS75DYbjQcZxNePY4BJdimXZ7XjZJk2yNDarFmMRfmUCbE'
rescind2 = '5AXpjQeFb5DSjP7a6p7fqXpbXVq4uC9CndwijrPXUrqvGpysvQkarW9tzmbiHjtEAQdcwmAodVe7xcF9MgMWEZie'

#Test Extended Loan:
extended1 = '2XF67zhawXvATey2i56PezgHPC1zQTwkMUNbuWBr5CjShquhuR7wc3DfbNd3nBTyFPW4SGdJwSehoWY7sf3MEzcN'
extended2 = '3UYsPKyTUFjb9kNp8EL2ydyGLbJ9zY8UcY4TadvDM7ZzQwYSFRk8XC5bGr6Usf4Az28GEAaHyHwiYs6JvcL1ucDY'


#Later, to get these txns run: 
"""
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getSignaturesForAddress",
    "params": [
        "SHARKobtfF1bHhxD2eqftjHBdVSCbKo9JtgK71FhELP", #SHARKY V1
        {
            "limit": "100"
        }
    ]
}

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Make the request
response = requests.post(url, headers=headers, data=json.dumps(payload))

"""


#Get transaction details


# Define the request payload
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTransaction",
    "params": [
        close1,
        "json"
    ]
}

# Make the request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Parse the response
response = response.json()

#Chain details
block_time = response['result']['blockTime']
fee = response['result']['meta']['fee']
fee_in_sol = fee/1e9
slot = response['result']['slot']

is_compute_budget = response['result']['meta']['logMessages'][0]


#Filter non-loan-related txns:
if 'ComputeBudget111111111111111111111111111111' in is_compute_budget:
    #print("yes")
    
    
    if 'TakeLoan' in response['result']['meta']['logMessages'][3]:
        print("Loan Taken !")
        
        #...DECODE
        ##Read more on inner instructions here: https://docs.solana.com/api/http#inner-instructions-structure
        instructions = response["result"]["meta"]["innerInstructions"]
        
        data = instructions[0]["instructions"][0]["data"]
        
        logs = response['result']['meta']['logMessages']

        for i in range(len(logs)):

            if "TransferAndFreezeCollateral" in logs[i]:
                #print((i, logs[i]))
                if i == 110:
                    loan_id = response['result']["transaction"]["message"]["accountKeys"][14]
                    print("Your loan ID is: " + loan_id)
                if i == 78:
                    loan_id = response['result']["transaction"]["message"]["accountKeys"][10]
                    print("Your loan ID is: " + loan_id)
                    
        
        
        
        
    if 'ForecloseLoan' in response['result']['meta']['logMessages'][3]:
        print("Loan closed !")
    
        print(response['result']['meta']['logMessages'])
        
        
    if 'ExtendLoan' in response['result']['meta']['logMessages'][3]:
        print("Loan extended !")
    
        #...DECODE
        
"""     
else:

    if 'RescindLoan' in response['result']['meta']['logMessages'][1]:
        print("Loan rescind!")

        #...DECODE
        
    if "ExtendLoanEscrow" #...
"""













