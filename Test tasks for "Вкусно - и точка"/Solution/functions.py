# Функции
def plot_for_test_task(df, number_id):

    # Выбираем номер id, для которого будем делать прогноз
    df = df[df['id'] == number_id].drop(['id'], axis=1)

    # Визуализируем данные временного ряда
    plt.figure(figsize=(15, 4))

    plt.title('Временной ряд с фактическими значениями для id = {}'.format(number_id))

    plt.plot(df[val_col], label='Фактическое значение', color=(1.0, 0.0, 0.5))

    plt.xlabel('Дата')
    plt.ylabel('Значения')

    plt.legend(loc='best')
    plt.grid(True)
    
    plt.show()

    def plot_moving_avg(series, window):

        rolling_mean = series.rolling(window=window).mean()
        rolling_std = df.rolling(window=window).std()
        
        plt.figure(figsize=(15, 4))
        plt.title('Среднее скользящее для id = {}, размер окна = {}'.format(number_id, window))

        plt.plot(series[window:], label='Фактическое значение', color='black')
        plt.plot(rolling_mean, label='Скользящий средний тренд', color=(1.0, 0.0, 0.5))
        plt.plot(rolling_std, label='Скользящее среднеквадратичное отклонение', color='b')

        plt.xlabel('Дата')
        plt.ylabel('Значения')
        
        plt.legend(loc='best')
        plt.grid(True)

    # чем шире окно, тем более плавный тренд
    plot_moving_avg(df, window=28)

    # Если мы хотим спрогнозировать данные на месяц вперед, то имеет смысл рассмотреть месячную сезонность. 
    # Поскольку у вас есть ежедневные данные, месячная сезонность будет 28 дней, в зависимости от месяца.
    decompose = seasonal_decompose(df, period=28)

    # Рисуем графики с измененными цветами
    fig, ax = plt.subplots(3, 1, figsize=(15, 15))

    # График тренда
    ax[0].plot(decompose.trend.index, decompose.trend, color='black')
    ax[0].set_ylabel('График тренда')

    # График сезонности
    ax[1].plot(decompose.seasonal.index, decompose.seasonal, color=(1.0, 0.0, 0.5))
    ax[1].set_ylabel('График сезонности')

    # График остатков
    ax[2].plot(decompose.resid.index, decompose.resid, color='blue')
    ax[2].set_ylabel('График остатков')
    
    plt.show()


def test_for_test_task(df, number_id):

    # Выбираем номер id, для которого будем делать прогноз
    df = df[df['id'] == number_id].drop(['id'], axis=1)

    # Одним из самых простых методов, которые мы можем использовать для предсказания следующего момента, 
    # является среднее арифметическое для всех ранее наблюдаемых точек данных

    def average(series):
        return np.mean(series)

    series = df[val_col]
    print('Cреднее арифметическое для всех ранее наблюдаемых точек данных:', average(series), '\n')

    # Вторым из простых методов, которые мы можем использовать для предсказания следующего момента, 
    # является среднее арифметическое для последних n пунктов, обосновывая это тем, что рассмотрение всех предыдущих точек данных будет добавлять шум

    def moving_average(series, n):
        return np.mean(series[-n:])

    # прогноз на последние 28 дней
    print('Cреднее арифметическое для последних n пунктов:', moving_average(series, 28), '\n')

    # Для более точной оценки стационарности можно применить тест Дики-Фуллера (Dickey-Fuller test). 
    # В данном случае гипотезы звучат следующим образом:
    # Нулевая гипотеза предполагает, что процесс нестационарный
    # Альтернативная гипотеза соответственно говорит об обратном

    dftest = adfuller(df[val_col], autolag='AIC')

    dfoutput = pd.Series(dftest[0:4], index=['Тестовая статистика','p-value','Используемые лаги','Количество использованных наблюдений'])
    for key,value in dftest[4].items():
        dfoutput['Критические значения (%s)'%key] = value
        
    print(dfoutput, '\n')

    # Если p-значение теста КПСС (KPSS) меньше выбранного уровня значимости (например, 0.05), 
    # то это указывает на нестационарность ряда. Если p-значение больше уровня значимости, то это может быть признаком стационарности.

    # КПСС-тест на стационарность
    kpss_test = kpss(df[val_col])
    print('KPSS Statistic:', kpss_test[0])
    print('p-value:', kpss_test[1])
    print('Critical Values:', kpss_test[3])

    if kpss_test[1] < 0.05:
        print('Ряд не стационарен')
    else:
        print('Ряд стационарен')

    # Ошибка, которую мы получаем, указывает на то, что статистика теста KPSS выходит за пределы диапазона доступных p-значений в таблице для поиска. 
    # Это означает, что ваш временной ряд имеет очень сильную сезонность или тренд, что делает интерпретацию результатов теста невозможной.

    # Каталогический анализ:
    # Если коррелограммы автокорреляции и частичной автокорреляции быстро уменьшаются и попадают 
    # в диапазон доверительных интервалов, это может указывать на стационарность.

    # Визуализация автокорреляционной функции (ACF) и частичной автокорреляции

    plot_acf(df[val_col])
    plot_pacf(df[val_col])
    plt.show()

    # То, что корреляция постоянно положительная говорит о наличии тренда.

    # Также замечу, что синяя граница позволяет оценить статистическую значимость корреляции. Если столбец выходит за ее пределы, 
    # то автокорреляция достаточно сильна и ее можно использовать при построении модели.

def examination_for_test_task(df, number_id):

    # Выбираем номер id, для которого будем делать прогноз
    df = df[df['id'] == number_id].drop(['id'], axis=1)

    # Для устранения нестационарности временного ряда можно использовать различные методы, такие как дифференцирование, 
    # логарифмирование, сглаживание или преобразование Бокса-Кокса

    df['val'] = np.log(df['val'])

    # Разделяем данные на тренировочные и тестовые для проверки качества предсказания
    df_train = df.loc[:'2021-12-26']
    df_test = df.loc['2021-12-26':]

    # обучим модель с соответствующими параметрами, SARIMAX(3, 0, 0)x(0, 1, 0, 12) 
    # создадим объект этой модели
    model = SARIMAX(df_train, order = (3, 0, 0), 
                    seasonal_order = (0, 1, 0, 12))
    
    # применим метод fit
    result = model.fit(disp=False)

    # тестовый прогнозный период начнется с конца обучающего периода
    start = len(df_train)
    # и закончится в конце тестового
    end = len(df_train) + len(df_test) - 1
    
    # применим метод predict
    predictions = result.predict(start=start, end=end)

    # Построим первый график
    plt.figure(figsize=(15, 4))

    # выведем три кривые (обучающая, тестовая выборка и тестовый прогноз)
    plt.plot(df_train, color = "black", label='train')
    plt.plot(df_test, color = (1.0, 0.0, 0.5), label='test')
    plt.plot(df_test.index, predictions, color = "b", label='predictions')
    
    # заголовок и подписи к осям
    plt.title("Обучающая выборка, тестовая выборка и тестовый прогноз")

    plt.xlabel('Дата')
    plt.ylabel('Значения')
    
    plt.legend(loc='best')
    plt.grid(True)
    
    plt.show()

    # Построим второй график
    plt.figure(figsize=(15, 4))

    plt.plot(df_test, label='test', color = (1.0, 0.0, 0.5))
    plt.plot(df_test.index, predictions, label='prediction', color = "b")

    plt.title("Тестовая выборка и тестовый прогноз")

    plt.xlabel('Дата')
    plt.ylabel('Значения')

    plt.legend(loc='best')
    plt.grid(True)

    plt.show()

    print('MSE на обычной шкале:', mean_squared_error(df_test, predictions))
    print('RMSE на обычной шкале:', np.sqrt(mean_squared_error(df_test, predictions)))
    print('MSE на логарифмической шкале:', mean_squared_log_error(df_test, predictions))

def plot_predict_for_test_task(df, df_new_test, number_id, date_with_start_for_plot):

    # Выбираем номер id, для которого будем делать прогноз
    df = df[df['id'] == number_id].drop(['id'], axis=1)

    # Для устранения нестационарности временного ряда можно использовать различные методы, такие как дифференцирование, 
    # логарифмирование, сглаживание или преобразование Бокса-Кокса

    df['val'] = np.log(df['val'])

    df_new_test = df_new_test[df_new_test['id'] == number_id].drop(['id'], axis=1).set_index('dt')

    # обучим модель с соответствующими параметрами, SARIMAX(3, 0, 0)x(0, 1, 0, 12) 
    # создадим объект этой модели
    model = SARIMAX(df, order = (3, 0, 0), 
                    seasonal_order = (0, 1, 0, 12))
    
    # применим метод fit
    result = model.fit(disp=False)

    # прогнозный период с конца имеющихся данных
    start_future = len(df)
    end_future = (len(df) - 1) + 28
    
    # теперь построим прогноз
    forecast = result.predict(start=start_future, end=end_future)

    # Построим первый график
    plt.figure(figsize=(15, 4))

    # выведем три кривые (обучающая, тестовая выборка и тестовый прогноз)
    plt.plot(df, color = "black", label='train')
    plt.plot(pd.to_datetime(df_new_test.index), forecast, color = (1.0, 0.0, 0.5), label='predictions')
    
    # заголовок и подписи к осям
    plt.title('Прогноз на будущее')
    plt.xlabel('Дата')
    plt.ylabel('Значения')
    
    plt.legend(loc='best')
    plt.grid(True)
    
    plt.show()

    # Построим второй график
    plt.figure(figsize=(15, 4))

    # выведем три кривые (обучающая, тестовая выборка и тестовый прогноз)
    plt.plot(df.loc[date_with_start_for_plot:], color = "black", label='train')
    plt.plot(pd.to_datetime(df_new_test.index), forecast, color = (1.0, 0.0, 0.5), label='predictions')

    plt.xlabel('Дата')
    plt.ylabel('Значения')

    plt.legend(loc='best')
    plt.grid(True)

    plt.show()