import os
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter


load_dotenv()

root_dir = os.getenv('root_dir')
if root_dir == '' or root_dir == None:
    root_dir = os.getcwd()

    
os.chdir(f'{root_dir}/outputs') # WD where output CSV file is


df = pd.read_csv('X2Y2_Loans_199423.csv')

#df.head()

df_nftfi = df[df['venue'] == 'NFTFi']
df_x2y2 = df[df['venue'] == 'X2Y2']

"""
print('\n')
weth_trades = df_nftfi[df_nftfi['paymentToken'] == 'WETH']
print(f'WETH total volume: {round(sum(weth_trades.maxRepayment), 1):,}')
print('\n')


dai_trades = df_nftfi[df_nftfi['paymentToken'] == 'DAI']
print(f'DAI total volume: {round(sum(dai_trades.maxRepayment), 1):,}')
print('\n')


usdc_trades = df_nftfi[df_nftfi['paymentToken'] == 'USDC']
print(f'USDC total volume: {round(sum(usdc_trades.maxRepayment), 1):,}')

print('\n')
print('\n')

bayc_loans_weth = df_nftfi[(df_nftfi['collateralContract'] == '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D') & (df_nftfi["paymentToken"] == 'WETH')]
print(f'BAYC WETH total volume: {round(sum(bayc_loans_weth.maxRepayment), 1):,}')
print('\n')

artblocks_loans_usdc = df_nftfi[(df_nftfi['collateralContract'] == '0xa7d8d9ef8D8Ce8992df_nftfi33D8b8CF4Aebabd5bD270') & (df_nftfi["paymentToken"] == 'USDC') ]
print(f'Art Blocks USDC total volume: {round(sum(artblocks_loans_usdc.maxRepayment), 1):,}')
print('\n')


wpunks_loans_dai = df_nftfi[(df_nftfi['collateralContract'] == '0xb7F7F6C52F2e2fdb1963Eab30438024864c313F6') & (df_nftfi["paymentToken"] == 'DAI')]
print(f'Wrapped Punks DAI total volume: {round(sum(wpunks_loans_dai.maxRepayment), 1):,}')
print('\n')


"""

"""
weth_trades = df_nftfi[df_nftfi['paymentToken'] == 'WETH']
effective_weth = weth_trades[(weth_trades["effectiveRate"] != '-') ]
effective_weth_rate = effective_weth['effectiveRate'].astype('float64').mean()
print(f"WETH efective rate on NFTFi: "+ str(effective_weth_rate))


#active_loans_x2y2 = df_x2y2[df_x2y2['status'] == 'active']

#print("X2Y2 Active loans:" + str(len(active_loans_x2y2)))
"""


spec_loan = df_nftfi[(df_nftfi['lender'] == '0xBbB589796d01EF05f24C49f57d53125d4382ab62') & (df_nftfi['borrower'] == '0xB26b5d90c8961a779efc8d8Ad881B128dD8385eB')]

spec_loan_lender = df_nftfi[df_nftfi['lender'] == '0xBbB589796d01EF05f24C49f57d53125d4382ab62']
spec_loan_borrower = df_nftfi[df_nftfi['borrower'] == '0xB26b5d90c8961a779efc8d8Ad881B128dD8385eB']


spec_loan_lender = spec_loan_lender[spec_loan_lender['status'] == 'expired']


"""
#Real rates of repaid trades
repaid_df = df[df['status'] == 'repaid']

repaid_df['effectiveRate'] = repaid_df['effectiveRate'].astype(float)
repaid_df = repaid_df.reset_index() 

repaid_df["effectiveAnualRate"] = ((1 + (repaid_df['effectiveRate']  /  repaid_df['loanDuration'] )) ** 365 ) -1
#( ((1 + repaid_df['effectiveRate']) ** (360 / repaid_df['loanDuration'])) - 1 )*100
#repaid_df["effectiveAnualRate"] = ((((repaid_df['effectiveRate']/repaid_df['loanDuration'])+1)**365)-1);


weth_rates = repaid_df[repaid_df['paymentToken'] == 'WETH']
weth_rates["effectiveAnualRate"].quantile(0.95).mean() * 100 


dai_rates = repaid_df[repaid_df['paymentToken'] == 'DAI']
dai_rates["effectiveAnualRate"].quantile(0.99)


usdc_rates = repaid_df[repaid_df['paymentToken'] == 'USDC']
usdc_rates["effectiveAnualRate"].mean() * 100
print(f"USDC mean APY on NFTFi: " + str(usdc_rates["effectiveAnualRate"].mean() * 100))
print(f"WETH mean APY on NFTFi: " + str(weth_rates["effectiveAnualRate"].quantile(0.95).mean() * 100 ))

"""

"""

#LOAN VOLUME
df_nftfi_usdc = df_nftfi[df_nftfi['paymentToken'] == 'USDC']
df_nftfi_usdc = df_nftfi_usdc[['loanStart', 'maxRepayment']]
df_nftfi_usdc['day'] =  pd.to_datetime(df_nftfi_usdc["loanStart"]).dt.strftime("%Y-%m-%d")
df_nftfi_usdc = df_nftfi_usdc.groupby('day').sum()[['maxRepayment']]

df_nftfi_dai = df_nftfi[df_nftfi['paymentToken'] == 'DAI']
df_nftfi_dai = df_nftfi_dai[['loanStart', 'maxRepayment']]
df_nftfi_dai['day'] =  pd.to_datetime(df_nftfi_dai["loanStart"]).dt.strftime("%Y-%m-%d")
df_nftfi_dai = df_nftfi_dai.groupby('day').sum()[['maxRepayment']]


df_nftfi_weth = df_nftfi[df_nftfi['paymentToken'] == 'WETH']
df_nftfi_weth = df_nftfi_weth[['loanStart', 'maxRepayment']]
df_nftfi_weth['day'] =  pd.to_datetime(df_nftfi_weth["loanStart"]).dt.strftime("%Y-%m-%d")
df_nftfi_weth = df_nftfi_weth.groupby('day').sum()[['maxRepayment']]



df_merged = pd.DataFrame()
df_merged['dt'] = pd.to_datetime(df_nftfi["loanStart"])
df_merged['day'] = pd.to_datetime(df_nftfi["loanStart"]).dt.strftime("%Y-%m-%d")
df_merged['USDC'] = df_merged.merge(df_nftfi_usdc, how='left', on='day')['maxRepayment']
df_merged['DAI'] = df_merged.merge(df_nftfi_dai, how='left', on='day')['maxRepayment']
df_merged['WETH'] = df_merged.merge(df_nftfi_weth, how='left', on='day')['maxRepayment'] *2300

df_merged = df_merged.set_index(pd.DatetimeIndex(df_merged['dt'].values))

#df_merged = df_merged[df_merged['dt'] >= '2023-01-01']

# sort the index
df_merged.sort_index(inplace=True)

# create data
x = df_merged['day']
y1 = df_merged['USDC']
y2 = df_merged['DAI']
y3 = df_merged['WETH']


def thousands_formatter(x, pos):
    if x/1000000 > 1:
        return f'{round(x / 1000000, 2)}Mn'
    if x/1000 > 1:
        return f'{round(x / 1000, 2)}k'
    else:
        return f'{round(x)}'
    
    
    
fig, ax = plt.subplots()

ax.plot(df_merged['dt'], y2, color = '#ffe700')
ax.plot(df_merged['dt'], y3, color = '#49b65a')
ax.plot(df_merged['dt'], y1, color='b')

ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

days = mdates.DayLocator(interval=90)
days_fmt = mdates.DateFormatter('%Y-%m')
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(days_fmt)
ax.set_ylabel('USD Volume')

plt.xticks(rotation=90, fontsize='x-small')
plt.legend([ 'DAI', 'WETH', 'USDC'])

plt.title("(WETH is estimaded at a fixed conversin rate of $2,300)",fontsize=12)
plt.suptitle("NFTFI's USD Volume by settlement token",fontsize=20, y=1.01)
plt.show()




# LOAN COUNT
x = pd.to_datetime(df_nftfi["loanStart"])
y = df_nftfi['paymentToken']


pd.crosstab(x.dt.to_period('M'), y).plot.bar(stacked=True,  color=['#ffe700', 'b', '#49b65a'])
plt.suptitle("NFTFi loans by settlement token",fontsize=20, y=1.01)
plt.xticks(rotation=90, fontsize='x-small')
plt.ylabel("Generated Loans")
plt.xlabel("Month")

plt.show()

"""









##X2Y2

#LOAN VOLUME
"""
df_x2y2_weth = df_x2y2[df_x2y2['paymentToken'] == 'WETH']
df_x2y2_weth = df_x2y2_weth[['loanStart', 'maxRepayment']]
df_x2y2_weth['day'] =  pd.to_datetime(df_x2y2_weth["loanStart"]).dt.strftime("%Y-%m-%d")

df_x2y2_weth = df_x2y2_weth.groupby('day').sum()[['maxRepayment']] * 2300

df_x2y2_weth = df_x2y2_weth.reset_index()
df_x2y2_weth['dt'] = pd.to_datetime(df_x2y2_weth['day'])

# create data
x = df_x2y2_weth['dt']
y3 = df_x2y2_weth['maxRepayment']


def thousands_formatter(x, pos):
    if x/1000000 > 1:
        return f'{round(x / 1000000, 2)}Mn'
    if x/1000 > 1:
        return f'{round(x / 1000, 2)}k'
    else:
        return f'{round(x)}'
    
    
    
fig, ax = plt.subplots()

ax.plot(x, y3, color = '#49b65a')

ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

days = mdates.DayLocator(interval=29)
days_fmt = mdates.DateFormatter('%Y-%m')
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(days_fmt)
ax.set_ylabel('USD Volume')

plt.xticks(rotation=90, fontsize='x-small')
plt.legend(['WETH'])

plt.title("(WETH is estimaded at a fixed conversin rate of $2,300)",fontsize=12)
plt.suptitle("X2Y2's USD Volume by settlement token",fontsize=20, y=1.01)
plt.show()




# LOAN COUNT
x = pd.to_datetime(df_x2y2["loanStart"])
y = df_x2y2['paymentToken']


pd.crosstab(x.dt.to_period('M'), y).plot.bar(stacked=True,  color=['#49b65a'])
plt.suptitle("X2Y2 loans by settlement token",fontsize=20, y=1.01)
plt.xticks(rotation=90, fontsize='x-small')
plt.ylabel("Generated Loans")
plt.xlabel("Month")

plt.show()


"""

















