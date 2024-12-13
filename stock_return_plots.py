import pandas as pd
def load_ff3(val_start_date=None, val_end_date=None):
    ff3 = pd.read_csv("ff3_daily.csv")

    if val_start_date is not None:
        val_start_idx = ff3[ff3['date'] >= int(val_start_date)].index[0]
        
    if val_end_date is not None:
        val_end_idx = ff3[ff3['date'] > int(val_end_date)].index[0]
    
    if val_start_date is not None and val_end_date is not None:
        ff3 = ff3.iloc[val_start_idx:val_end_idx]
    elif val_start_date is not None:
        ff3 = ff3.iloc[val_start_idx:]
    elif val_end_date is not None:
        ff3 = ff3.iloc[:val_end_idx]
    

    ff3 = ff3.reset_index(drop=True)
    ff3.index = ff3["date"]
    ff3 = ff3.drop(columns=["date"])

    return ff3

def load_china(val_start_date=None, val_end_date=None):
    china = pd.read_csv("china_daily.csv")

    if val_start_date is not None:
        val_start_idx = china[china['date'] >= int(val_start_date)].index[0]
        
    if val_end_date is not None:
        val_end_idx = china[china['date'] >= int(val_end_date)].index[0]
    
    if val_start_date is not None and val_end_date is not None:
        china = china.iloc[val_start_idx:val_end_idx]
    elif val_start_date is not None:
        china = china.iloc[val_start_idx:]
    elif val_end_date is not None:
        china = china.iloc[:val_end_idx]
    

    china = china.reset_index(drop=True)
    china.index = china["date"]
    china = china.drop(columns=["date"])

    return china
ff3 = load_ff3("20000104", "20211231")
ff3.info()
us_mkt_ret_vec = ff3["Mkt-RF"] + ff3["RF"]
us_mkt_ret_vec.head()
import matplotlib.pyplot as plt
import os
def show_cumulative_returns(
    strat_ret_vec,
    mkt_ret_vec,
    ret_port_style,
    strategy_name="Strategy",
    market_name="US Market",
    log_scale=False,
    show_plots=False,
    save=False,
):
    cum_strat_rets = (1 + strat_ret_vec / 100).cumprod()
    cum_mkt_rets = (1 + mkt_ret_vec / 100).cumprod()

    cum_mkt_rets.index = pd.to_datetime(cum_mkt_rets.index, format="%Y%m%d")
    cum_mkt_rets_monthly = cum_mkt_rets.resample("M").last()

    cum_strat_rets.index = pd.to_datetime(cum_strat_rets.index, format="%Y%m%d")
    cum_strat_rets_monthly = cum_strat_rets.resample("M").last()

    if show_plots:
        # fig, axs = plt.subplots(2, 1, figsize=(12, 6))
        fig, axs = plt.subplots(1, 1, figsize=(12, 6))
        # Plot the cumulative returns
        axs.plot(cum_strat_rets, label=strategy_name)
        axs.plot(cum_mkt_rets, label=market_name)

        if log_scale:
            axs.yscale("log")
        axs.set_xlabel("Year")
        axs.set_ylabel("Cumulative Return")
        axs.legend()
        axs.set_title(f"Returns Portfolio Style: {ret_port_style}")

        strat_ret_vec_monthly = strat_ret_vec.copy()
        strat_ret_vec_monthly.index = pd.to_datetime(strat_ret_vec_monthly.index, format="%Y%m%d")
        strat_ret_vec_monthly = strat_ret_vec_monthly.resample('Y').apply(lambda x: (x/100 + 1).prod() - 1)
        
        mkt_ret_vec_monthly = mkt_ret_vec.copy()
        mkt_ret_vec_monthly.index = pd.to_datetime(mkt_ret_vec_monthly.index, format="%Y%m%d")
        mkt_ret_vec_monthly = mkt_ret_vec_monthly.resample('Y').apply(lambda x: (x/100 + 1).prod() - 1)
        
        # x = np.arange(len(strat_ret_vec_monthly.index))
        
        # num_ticks = 7
        # tick_positions = np.linspace(0, len(x) - 1, num_ticks, dtype=int)
        # tick_labels = strat_ret_vec_monthly.index[tick_positions].strftime('%Y')

        # barwidth = 0.2
        
        # axs[1].bar(x - barwidth/2, strat_ret_vec_monthly.values, label=strategy_name, width=barwidth )
        # axs[1].bar(x + barwidth/2, mkt_ret_vec_monthly.values, label="Market", width=barwidth)
        # axs[1].set_xlabel("Year")
        # axs[1].set_ylabel("Yearly Return")
        # axs[1].legend()
        # axs[1].set_title(f"Returns Portfolio Style: {ret_port_style}")
        # axs[1].grid(axis='y', linestyle='--', alpha=0.7)
        
        # axs[1].set_xticks(tick_positions)
        # axs[1].set_xticklabels(tick_labels, rotation=90)

        plt.title(f"Returns Portfolio Style: {ret_port_style}")
        
        # Save plot
        if save:
            name = strategy_name.replace("models", "")
            os.makedirs(f"results/{name}/{ret_port_style}", exist_ok=True)
            plt.savefig(f"results/{name}/{ret_port_style}/cumulative_returns.png")

        plt.show()

    # Save the plot
    if save:
        name = strategy_name.replace("models", "")
        os.makedirs(f"results/{name}/{ret_port_style}", exist_ok=True)

        # save cum_strat_rets in csv
        cum_strat_rets.to_frame().to_csv(
            f"results/{name}/{ret_port_style}/cumulative_returns.csv"
        )

        # save strat_ret_vecs in csv
        strat_ret_vec.to_frame().to_csv(
            f"results/{name}/{ret_port_style}/strat_ret_vec.csv"
        )
show_cumulative_returns(us_mkt_ret_vec, us_mkt_ret_vec, ret_port_style="S&P 500 Market", log_scale=False, show_plots=True, save=True)
china = load_china("20000104", "20211231")
china.info()
china_mkt_ret_vec = china["mktrf"] + china["rf_dly"]
china_mkt_ret_vec.head()
show_cumulative_returns(china_mkt_ret_vec, us_mkt_ret_vec, ret_port_style="Chinese Market", strategy_name="China Market", log_scale=False, show_plots=True, save=True)
def plotting(start_date, val_date):
    ff3 = load_ff3(start_date, val_date)
    china = load_china(start_date, val_date)
    us_mkt_ret_vec = ff3["Mkt-RF"] + ff3["RF"]
    china_mkt_ret_vec = china["mktrf"] + china["rf_dly"]

    show_cumulative_returns(china_mkt_ret_vec, us_mkt_ret_vec, ret_port_style="Chinese Market", strategy_name="China Market", log_scale=False, show_plots=True, save=True)

# Just change this to be the correct dates
plotting("20200101", "20211231")
