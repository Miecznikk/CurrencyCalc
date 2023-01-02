import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

class NbpApi:
    codes = ['USD','AUD','EUR']
    table = 'A'
    rates = {
        'USD' : {},
        'AUD' : {},
        'EUR' : {}
    }
    last_rates_dates = {
        'USD' : 0,
        'AUD' : 0,
        'EUR' : 0
    }
    actual_rates = {
        'USD' : 0,
        'AUD' : 0,
        'EUR' : 0
    }
    intervals = ['1m','3m','6m','1y','3y']

    def __init__(self):
        self.get_actual_rates()
        self.get_rates()

    def get_actual_rates(self):
        for code in self.codes:
            response = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/{self.table}/{code}/')
            if response.status_code == 200:
                self.actual_rates[code] = response.json()['rates'][0]['mid']
                self.last_rates_dates[code] = response.json()['rates'][0]['effectiveDate']

    def get_rates(self):
        for code in self.codes:
            self.get_n_days_rates(code,30,'1m')
            self.get_n_days_rates(code,90,'3m')
            self.get_n_days_rates(code,180,'6m')
            self.get_n_days_rates(code,365,'1y')
            self.get_3_years_rates(code)
        self.draw_plots()

    def get_n_days_rates(self,code,n,interval):
        st_date = dt.datetime.strptime(self.last_rates_dates[code],'%Y-%m-%d').date() - dt.timedelta(days = n)
        response = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/{self.table}/{code}/{st_date}/{self.last_rates_dates[code]}/')
        if response.status_code == 200:
            json = response.json()['rates']
            self.rates[code][interval] = [{'date': rate['effectiveDate'], 'rate':rate['mid']} for rate in json]

    def get_3_years_rates(self,code):
        arr = []
        st_date = dt.datetime.strptime(self.last_rates_dates[code],'%Y-%m-%d').date() - dt.timedelta(days = 365)
        response = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/{self.table}/{code}/{st_date}/{self.last_rates_dates[code]}/')
        arr += [{'date': rate['effectiveDate'], 'rate': rate['mid']} for rate in response.json()['rates']][::-1]
        for i in range(2):
            end_date = st_date - dt.timedelta(days = 1)
            st_date = st_date - dt.timedelta(days = 365)
            response = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/{self.table}/{code}/{st_date}/{end_date}/')
            if response.status_code == 200:
                arr += [{'date': rate['effectiveDate'], 'rate': rate['mid']} for rate in response.json()['rates']][::-1]
        self.rates[code]['3y'] = arr[::-1]

    def draw_plots(self):
        locator_intervals = {
            '1m': 6,
            '3m': 18,
            '6m': 36,
            '1y': 65,
            '3y': 180
        }
        for code in self.codes:
            for interval in self.intervals:
                rates = self.rates[code][interval]
                file_path = f'images/{code}/{interval}.png'
                x_axis = [dt.datetime.strptime(rate['date'],'%Y-%m-%d') for rate in rates]
                y_axis = [rate['rate'] for rate in rates]
                fig = plt.figure()
                fig.patch.set_facecolor('#FAFAFA')
                plt.xlabel("Data")
                plt.ylabel("Kurs (zł)")
                plt.xticks(fontsize=8)
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
                plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=locator_intervals[interval]))
                plt.plot(x_axis, y_axis)
                plt.savefig(file_path)
                plt.clf()

        return True

nbp_api = NbpApi()




