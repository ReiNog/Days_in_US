# Service to control the number of days the user can spend in the US without triggering fiscal residency
import pandas as pd

def get_user_id():
    user_id = "rbnmls"
    return(user_id)

def load_days_spent(db_path='.\\Data\\user_days_usa.csv', range_years=[2020,2021,2022,2023,2024,2025]):
    try:
        days_spent = pd.read_csv(db_path, index_col=0)
    except OSError as err:
        # if there is no file, I assume it is the first time que user is using the app
        days_spent = pd.DataFrame(data={'days_spent':[0,0,0,0,0,0],'days_to_spend':[0,0,0,120,120,120]},index=range_years)
    except Exception as err:
        raise(err)

    return(days_spent)

def get_new_spent_days(ctrl_days_spent):
    # placeholder to get input from user
    ctrl_days_spent['days_spent']=[0,0,14,0,0,0]
    return(ctrl_days_spent)

def calc_new_days_to_spend(ctrl_days_spent, max_days):
    ctrl_days_spent['days_to_spend'] = round(max_days - ctrl_days_spent['days_spent'] - ctrl_days_spent['days_spent'].shift(1) / 3 - ctrl_days_spent['days_spent'].shift(2) / 6, 0)
    # update the first 2 rows becanme NaN
    ctrl_days_spent.at[ctrl_days_spent.first_valid_index(),'days_to_spend'] = round(max_days - ctrl_days_spent.at[ctrl_days_spent.first_valid_index(),'days_spent'], 0)
    ctrl_days_spent.at[ctrl_days_spent.first_valid_index() + 1,'days_to_spend'] = round(max_days - ctrl_days_spent.at[ctrl_days_spent.first_valid_index() + 1,'days_spent'] - ctrl_days_spent.at[ctrl_days_spent.first_valid_index(),'days_spent'] / 3, 0)
    return(ctrl_days_spent)

def write_days_spent(ctrl_days_spent, db_path='.\\Data\\user_days_usa.csv'):
    ctrl_days_spent.to_csv(db_path, index_label='year')

def main():
    # Max number of days to stay in the US without triggering fiscal residency is 182
    max_days = 182
    # A range of 6 years serves well for the majority of people. The range must always start 2 years before the current year
    range_years = [2020,2021,2022,2023,2024,2025]
    user_id = get_user_id()
    db_path = ".\\Data\\" + user_id + "_days_usa.csv"

    days_in_usa = load_days_spent(db_path, range_years)
    days_in_usa = get_new_spent_days(days_in_usa)
    days_in_usa = calc_new_days_to_spend(days_in_usa, max_days)
    write_days_spent(days_in_usa, db_path)
