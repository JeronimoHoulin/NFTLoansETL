import requests
import json

url = "https://api.mainnet-beta.solana.com"

# Set the headers
headers = {
    "Content-Type": "application/json"
}


#Test loans:
loan1 = '5zm3R6HCWkj6m5UzzHHWoAtcbxLqEnazzeeX7GVV9wuet3V2nS8wfo8uAK8hTkT4JBHn1LVPVrkgB1nqFDqh7yjr'
loan2 = '4f8CzWjdLeM9bwBFy9QLrrwAAQhYMmV5pJ9CbRRLXsrPuKbZJ65muALZn8cyfdNxora2GTw94gPwduC3dfiHCYHr'
loan3 = '2wDpyy7SuYTBxfhYS39LjjdnBMcZrZ5RbkT1Nrtc9qaiJfH2NXwhRpGFQaZFyeCdEfE77ApRkHJ5M5oK9zXrDtgF' 

#Test pay back loans:
close1 = 'ZtBY1yGnDFwqYJNAP2BXRXb82ga6WRfe9B4g7swGupVjYF38YaYw3GTpx6Ln2dj67MhNqK9qoQfcfYGG7RSVpVW'
close2 = 'KPtGFXpm5mBQfx7H3uiBNAvXJ1ahsp47r7vYHdXmjeqSRC9zV8NPSTCw6s1yxxWkFeaVDj5dr7GmnJwDHERqZwe'
close3 = '3iWbvcaLbKKkepZ812khrUuXUgf4S23yQq39egNxbvQ6V618khypEqN2aiDhZzpFvXLQ5iCoii4MAkXC2hNzi5gF'

reborrow1 = 'ZtBY1yGnDFwqYJNAP2BXRXb82ga6WRfe9B4g7swGupVjYF38YaYw3GTpx6Ln2dj67MhNqK9qoQfcfYGG7RSVpVW'
reborrow2 = 'KPtGFXpm5mBQfx7H3uiBNAvXJ1ahsp47r7vYHdXmjeqSRC9zV8NPSTCw6s1yxxWkFeaVDj5dr7GmnJwDHERqZwe'
reborrow3 = '3iWbvcaLbKKkepZ812khrUuXUgf4S23yQq39egNxbvQ6V618khypEqN2aiDhZzpFvXLQ5iCoii4MAkXC2hNzi5gF'

#Test liquidate Loan:
liquidate1 = '4iomdGyosRbVPb4K7DWhTeq81zMeKVCt4wTjbHZN25ESzkuBCZRNLvKUqSF8MfGqb1XWHhV5T5tK2RURvxfNejES'
liquidate2 = '3uMxKzDQC6fKAcPDzqqkXHy3Eaej32TVXKVWZrgZXUrivTCnd7HVSnHPBFia7yML7ajza3NVdNZfJu2BBuW9FobE'
liquidate3 = 'WK6vHShasjZzNA82uKMschsYFFZ8BEzrPNfeFLzZyVLYLoh5KrgY2dmUBcmhDLiPp3SuLKD22RoxZAJHoPZMbNQ'

#Later, to get these txns run: 
"""
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getSignaturesForAddress",
    "params": [
        "JCFRaPv7852ESRwJJGRy2mysUMydXZgVVhrMLmExvmVp", #Citrus V1
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
    
    
    if 'Lend' in response['result']['meta']['logMessages'][3]:
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
                    
        
        
        
        
    if 'repay' in response['result']['meta']['logMessages'][3]:
        print("Loan paid back !")
    
        print(response['result']['meta']['logMessages'])
        
        
    if 'Reborrow' in response['result']['meta']['logMessages'][3]:
        print("Loan re financed !")
    
        #...DECODE
    if 'Claim' in response['result']['meta']['logMessages'][3]:
        print("Loan defaulted !")
    
        #...DECODE
        
"""     
else:

    if 'RescindLoan' in response['result']['meta']['logMessages'][1]:
        print("Loan rescind!")

        #...DECODE
        
    if "ExtendLoanEscrow" #...
"""













