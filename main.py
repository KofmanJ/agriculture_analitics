import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_excel('data.xlsx', sheet_name='Y', header=3)
df.set_index('Year', inplace=True)

# Проверка содержания данных
# print(df)
# print(df.head())
# print(df.columns)


# Список колонок, для которых нужно сделать прогноз
columns_to_forecast = ['Soybeans', 'Phosphate rock', 'Sunflower oil', 'Wheat']

# Приводим данные к числовому типу
for column in columns_to_forecast:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Удаляем строки с пропущенными значениями
df_clean = df.dropna(subset=columns_to_forecast)


def forecast_prices(data, column, periods=7):
    try:
        # Фильтрация значений, пропуская None
        filtered_data = data[column].dropna()

        # Проверка, достаточно ли данных для прогнозирования
        if len(filtered_data) < 2:  # Измените это значение при необходимости
            print(f"Недостаточно данных для прогнозирования для '{column}'. Пропускаю.")
            return [None] * periods

        # Создание модели ARIMA
        model = ARIMA(filtered_data, order=(1, 1, 1))  # Подберите параметры ARIMA
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=periods)
        return forecast

    except Exception as e:
        print(f"Ошибка при прогнозировании для '{column}': {e}")
        return [None] * periods  # Возвращаем список из None в случае ошибки


# # Количество периодов для прогнозирования (с 2024 по 2030 — 7 лет)
# years_to_forecast = 7

# Создаём словарь для хранения прогнозов
forecasts = {}

for column in columns_to_forecast:
    forecasts[column] = forecast_prices(df_clean, column)
    # print(f"Прогнозы для '{column}': {forecasts[column]}")

# Вывод прогнозов
# print(forecasts)
# years = range(2024, 2031)
forecast_df = pd.DataFrame(forecasts)

# Сохранение результатов в CSV файл
forecast_df.to_csv('forecast_prices.csv', index=True)
