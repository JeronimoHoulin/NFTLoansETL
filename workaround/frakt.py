import requests
import json

url = "https://api.mainnet-beta.solana.com"

# Set the headers
headers = {
    "Content-Type": "application/json"
}


#Test loans:
loan1 = 'dokfh7a4vgXq1qe3SYUZXVFctA4RdqDtbd816e2xWkyZXcqTzGNQ9A5M2JePWpkaRbVHsevhKprVCpemd2VJymj'
loan2 = '5kj4qFqbfP6Pbz9KZs1NS64oysh49ygC2nXrrzrKTipC5hKBM4TDaYp1hsBpnAmgp9qNZtTTzUTxjqoEBtHq1UGJ'
loan3 = '22vzXXRkbuSVXWHc6gviFgXf7Ye1dKuQPu85wk3oNtD5WZia2bLq9AtK8EVE1MhYRDp5AzV8GHTZtgzXNCPmo5M1' 

#Test pay back loans:
close1 = '4d3MMTCnDfRofqpDTYPDa8drDzgARMx7vQfdCfhTRepbetz3WtpKRXFToVxcNBcX1PBbU85U2y7L41oV4StdLGqq'
close2 = '5WWkCdr6DSRTtxV2nsY3JQwJcgghSywh5C4U5t5D6FEw7PjkEMyaEHCuz3hN9PSYAhpDFSy6awJcKpb4HSRmbd8S'
close3 = '2o4v4YgEjvyG4DA82Sgkbod44iRySRMbBgJyAGdmCehTm8TRr2WPTHeGoqfBnGUmWkjdKXNuqo4C1EGy1LNXivic'

#Test liquidate Loan:
liquidate1 = '4D3JdBCtBtVTPqR3MszwA1V9n1ZWzKPrzjp4pkgN1NmZpup3qcL9smCzTyxJHmnkGFNoSgWgBJ5Ktv4J9LXbfFC2'
liquidate2 = '3TZrv9ztQNqsJPQ67ZBgmEKEgb7LXCkgpFkGmfGRzavHFRMsHYARzsJydtzFZqW5g8FjBB5ggsNg2vqr4VNJAmT'
liquidate3 = '3m9nR1HfBQ8L81cmGDbWNrDsVjj6Y43VDDJzVRMh179PZVD5wGtFEcMiFzCUPEzskQNpxpMrbPEkpFwyGVREg9Vp'

#Later, to get these txns run: 
"""
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getSignaturesForAddress",
    "params": [
        "A66HabVL3DzNzeJgcHYtRRNW1ZRMKwBfrdSR4kLsZ9DJ", #FRAKT V2
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
    
    
    if 'ApproveLoanByAdmin' in response['result']['meta']['logMessages'][3]:
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
                    
        
        
        
        
    if 'PaybackLoan' in response['result']['meta']['logMessages'][3]:
        print("Loan paid back !")
    
        print(response['result']['meta']['logMessages'])
        
        
    if 'LiquidateNftToRaffles' in response['result']['meta']['logMessages'][3]:
        print("Loan liquidated !")
    
        #...DECODE
        
"""     
else:

    if 'RescindLoan' in response['result']['meta']['logMessages'][1]:
        print("Loan rescind!")

        #...DECODE
        
    if "ExtendLoanEscrow" #...
"""













