import pandas as pd

from core.handler.data_base_handler import DataBaseHandler

def get_human_time_spent_of_all_zone(db:DataBaseHandler, human_id:int):
    # отримання розпізнаних користувачів
    persons = db.get_person_identification_log(human_id)
    df = pd.DataFrame(persons, columns=['log_id', 'value', 'attribute_name'])
    df_persons = df.pivot_table(index='log_id', columns='attribute_name', values='value', aggfunc='first').reset_index()
    if df_persons.empty:
        return None
    data = db.get_report_by_person_ids(list(df_persons["person_id"]))
    df = pd.DataFrame(data, columns=["row_id", "value", "column_name", "timestamp"])
    pivot_df = df.pivot(index="row_id", columns="column_name", values="value")
    pivot_df['timestamp'] = df.groupby('row_id')['timestamp'].first().values
    pivot_df.reset_index(inplace=True)
    df = pivot_df.sort_values(by='timestamp')

    # сумарний час у кожній зоні
    # Додаємо стовпець із днем
    df['date'] = df['timestamp'].dt.date
    # Додаємо стовпець із днем # Обчислюємо час, проведений у кожній зоні
    df['time_spent'] = df['timestamp'].diff().fillna(pd.Timedelta(seconds=0))
    # Групуємо за днем і зоною, підсумовуємо час
    daily_time_spent = df.groupby(['date', 'current_zone_id'])['time_spent'].sum().reset_index()
    # Перейменовуємо стовпці для ясності
    daily_time_spent.columns = ['Date', 'Zone', 'Time Spent']
    # daily_time_spent.to_csv("daily_time_spent.csv", sep=';', index=False)
    return daily_time_spent

if __name__ == "__main__":
    db = DataBaseHandler()
    df_result = pd.DataFrame()
    human_ids = [0,1,2,3]
    for human_id in human_ids:
        df_human_time_spent = get_human_time_spent_of_all_zone(db, human_id)
        if df_human_time_spent is None: continue
        df_human_time_spent["human_id"] = human_id
        df_result = pd.concat([df_result, df_human_time_spent], ignore_index=True)
    df_result.to_csv("result.csv", sep=';', index=False)
