import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA


df = pd.read_excel('data.xlsx', sheet_name='Y', header=3)
df.set_index('Year', inplace=True)
# df.index = pd.to_datetime(df.index, format='%Y', errors='coerce')  # Пример для годовых данных
# print(df.index)
# print(df)    # Проверка содержания данных
# print(df.head())
# print(df.columns)


# nan_check = df.isnull().sum()    # Проверка на значение None
# print(nan_check)


# Удаляем строки с пропущенными значениями
# df_cleaned = df.dropna(subset=['Soybeans', 'Phosphate rock', 'Sunflower oil', 'Wheat'])
# df_cleaned = df.dropna(subset=['Soybeans'])
# Список колонок, для которых нужно сделать прогноз
columns_to_forecast = ['Soybeans', 'Phosphate rock', 'Sunflower oil', 'Wheat']
# columns_to_forecast = ['Soybeans']
# Проверка данных по колонкам по всем годам
# col_df = df[['Soybeans', 'Phosphate rock', 'Sunflower oil', 'Wheat']]
# col_df.to_csv('col_df.csv', index=True)
# Проверка типов данных
# print(df[['Soybeans', 'Phosphate rock', 'Sunflower oil', 'Wheat']].dtypes)
# Приводим данные к числовому типу
for column in columns_to_forecast:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Удаляем строки с пропущенными значениями
df_clean = df.dropna(subset=columns_to_forecast)
# df_clean = df.dropna(subset='Soybeans')

# print(df['Soybeans', 'Phosphate rock', 'Sunflower oil', 'Wheat'].dtypes)
#
# nan_check = df[['Soybeans', 'Phosphate rock', 'Sunflower oil', 'Wheat']].isnull().sum()
# print(nan_check)
# col_df = df[['Soybeans', 'Phosphate rock', 'Sunflower oil', 'Wheat']]
# col_df.to_csv('col_df.csv', index=True)
# df.fillna(df.mean(numeric_only=True), inplace=True)


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
# print(forecasts)
# # years = range(2024, 2031)
# forecast_df = pd.DataFrame(forecasts)
# print(forecast_df)
# # print(forecast_df)
#
# forecast_df.to_csv('forecast_prices.csv', index=True)
#
forecasts = {
    'Soybeans': [564.02, 568.84, 568.15, 568.25, 568.24, 568.24, 568.24],
    'Phosphate rock': [303.87, 311.88, 308.27, 309.90, 309.17, 309.50, 309.35],
    'Sunflower oil': [955.63, 961.48, 964.43, 965.92, 966.67, 967.05, 967.24],
    'Wheat': [227.11, 221.09, 217.44, 215.24, 213.90, 213.09, 212.60]
}

# Создание индекса
years = range(2024, 2031)  # от 2024 до 2030

# Создаем DataFrame с пользовательским индексом
forecast_df = pd.DataFrame(forecasts, index=years)

# Проверка результатов
print(forecast_df)