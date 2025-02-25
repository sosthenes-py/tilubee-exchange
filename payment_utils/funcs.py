def bcdiv(amount, one_usd_in_base=None):
    """
    Returns a more significant figure for amount
    If one_usd_in_base is applied, returns amount in base currency
    """
    if one_usd_in_base is not None:
        amount = amount * one_usd_in_base

    if amount < 0.09:
        amt = f'{amount:.5f}'
    elif 0.09 <= amount < 1:
        amt = f'{amount:.3f}'
    else:
        amt = f'{amount:.2f}'
    return float(amt)

