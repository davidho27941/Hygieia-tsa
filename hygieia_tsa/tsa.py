from statsmodels.tsa.seasonal import seasonal_decompose

from statsmodels.tsa.stattools import (
    acf, 
    pacf, 
    adfuller, 
    kpss,
)

def generate_stl(data, period=1095):
    # 1095 = 365*3
    return seasonal_decompose(data, period=period)

def adf_test(data, nlags, regression='ct'):
    (
        test_stats,
        p_value,
        usedlag,
        n_obs,
        critical_values,
        icbest,
    ) = adfuller(
        data,
        maxlag=96,
        regression='ct'
    )

    reject_0_01 = True if p_value < critical_values['1%'] else False
    reject_0_05 = True if p_value < critical_values['5%'] else False
    reject_0_1 = True if p_value < critical_values['10%'] else False


    return {
        "test_stats": test_stats,
        "p_value": p_value,
        "usedlag": usedlag,
        "n_obs": n_obs,
        "critical_values": critical_values,
        "icbest": icbest,
        "reject_null@0.01": reject_0_01, 
        "reject_null@0.05": reject_0_05, 
        "reject_null@0.1": reject_0_1, 
    }
    
    
def kpss_test(data, nlags, regression='ct'):
    test_stats, p_value, lags, critical_values = kpss(
        data,
        nlags='auto',
        regression='ct'
    )

    reject_0_01 = True if p_value < critical_values['1%'] else False
    reject_0_025 = True if p_value < critical_values['2.5%'] else False
    reject_0_05 = True if p_value < critical_values['5%'] else False
    reject_0_1 = True if p_value < critical_values['10%'] else False


    return {
        "test_stats": test_stats,
        "p_value": p_value,
        "lags": lags,
        "critical_values": critical_values,
        "reject_null@0.01": reject_0_01, 
        "reject_null@0.05": reject_0_05, 
        "reject_null@0.025": reject_0_025, 
        "reject_null@0.1": reject_0_1, 
    }
    
def combine_adf_kpss(adf_result, kpss_result, target_threshold='reject_null@0.05'):
    
    need_detrend, need_difference = False, False

    match [adf_result[target_threshold], kpss_result[target_threshold]]:
        case [False, True]:
            not_stationary = True
            trended = False
        case [True, False]:
            not_stationary = False
            trended = False
        case [False, False]:
            not_stationary = False
            need_detrend = True
        case [True, True]:
            not_stationary = False
            need_difference = True
    
    return not_stationary, need_detrend, need_difference
      

def calc_acf(data, n_lags, alpha=0.05):
    acf_result, acf_confint = acf(
        data,
        nlags=n_lags,
        alpha=alpha,
    )
    
    acf_lower_bound = acf_confint[1:, 0] - acf_result[1:]
    acf_upper_bound = acf_confint[1:, 1] - acf_result[1:]
    
    return acf_result, (acf_lower_bound, acf_upper_bound)
    
def calc_pacf(data, n_lags, alpha=0.05):
    pacf_result, pacf_confint = pacf(
        data,
        nlags=n_lags,
        alpha=alpha,
    )
    
    pacf_lower_bound = pacf_confint[1:, 0] - pacf_result[1:]
    pacf_upper_bound = pacf_confint[1:, 1] - pacf_result[1:]
    
    return pacf_result, (pacf_lower_bound, pacf_upper_bound)