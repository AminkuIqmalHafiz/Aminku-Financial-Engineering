import numpy as np

def cal_rate_swap(discount_factors):
    df_array = np.array(discount_factors)
    final_df = df_array[-1]


    sum_df = np.sum(df_array)
    swap_rate = (1- final_df)/sum_df
    return swap_rate

curve = [0.95,0.90,0.86,0.89,0.78] # Supposed to be a stochastic yield curve
s = cal_rate_swap(curve)
print (f"The fair Rate Swap is: {s*100:.2f}%")
