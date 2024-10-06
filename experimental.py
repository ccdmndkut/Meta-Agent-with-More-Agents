from src.tool import tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from typing import List
load_dotenv()

class WebSearch(BaseModel):
    query: str = Field(..., description='The query to be searched.', example=['ADBE stock'])

@tool('Web Search Tool', args_schema=WebSearch)
def web_search_tool(query: str, max_results: int=5, retry_count: int=3, delay: float=1.0, user_agents: List[str]=None) -> str:
    """
    Searches for articles related to the given query using DDGS (DuckDuckGo Search) and returns the formatted results.
    """
    from duckduckgo_search import DDGS
    import os
    import time
    import random
    api_key = os.environ.get('DDGS_API_KEY')
    try:
        ddgs = DDGS()
        results = []
        retries = 0
        if user_agents is None:
            user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 Edge/16.16299']
        while len(results) < max_results and retries < retry_count:
            try:
                ddgs.user_agent = random.choice(user_agents)
                results.extend(ddgs.text(query, max_results=max_results - len(results)))
                time.sleep(delay)
            except Exception as err:
                retries += 1
                if 'rate limit' in str(err).lower():
                    time.sleep(delay * 2)
                else:
                    raise
        return '\n'.join([f'{result['title']}\n{result['body']}' for result in results])
    except Exception as err:
        return f'Error: {err}'

class AlphaVantageStock(BaseModel):
    symbol: str = Field(..., description='The stock symbol.', example=['ADBE'])

@tool('Alpha Vantage Stock Tool', args_schema=AlphaVantageStock)
def alpha_vantage_stock_tool(symbol: str):
    """
    Retrieves stock information for the given symbol using the Alpha Vantage API.
    """
    import requests
    import os
    import json
    api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    try:
        response = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}')
        data = response.json()
        if 'Global Quote' in data:
            return json.dumps(data['Global Quote'], indent=4)
        else:
            return 'No data found for the given symbol.'
    except Exception as err:
        return f'Error: {err}'

class StockInformation(BaseModel):
    ticker_symbol: str = Field(..., description='The ticker symbol of the stock.', example=['ADBE'])

@tool('Stock Information Tool', args_schema=StockInformation)
def stock_information_tool(ticker_symbol: str):
    """
    Gathers information on the given stock prices and trends from the web and provides insights on possible options to buy.
    """
    import yfinance as yf
    import pandas as pd
    import os
    from datetime import datetime
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        hist = stock.history(period='1y')
        current_price = info['currentPrice']
        fifty_two_week_high = info['fiftyTwoWeekHigh']
        fifty_two_week_low = info['fiftyTwoWeekLow']
        average_price = hist['Close'].mean()
        if current_price < average_price:
            recommendation = 'Buy'
        else:
            recommendation = 'Hold'
        return f'Current Price: {current_price}\n52 Week High: {fifty_two_week_high}\n52 Week Low: {fifty_two_week_low}\nAverage Price: {average_price}\nRecommendation: {recommendation}'
    except Exception as err:
        return f'Error: {err}'

class WebSearch(BaseModel):
    query: str = Field(..., description='The query to be searched.', example=['An example for search query'])

@tool('Web Search Tool', args_schema=WebSearch)
def web_search_tool(query: str, max_results: int=5, retry_count: int=3, delay: float=1.0, user_agents: List[str]=None) -> str:
    """
    Searches for articles related to the given query using DDGS (DuckDuckGo Search) and returns the formatted results.
    """
    from duckduckgo_search import DDGS
    import os
    import time
    import random
    api_key = os.environ.get('DDGS_API_KEY')
    try:
        ddgs = DDGS()
        results = []
        retries = 0
        if user_agents is None:
            user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 Edge/16.16299']
        while len(results) < max_results and retries < retry_count:
            try:
                ddgs.user_agent = random.choice(user_agents)
                results.extend(ddgs.text(query, max_results=max_results - len(results)))
                time.sleep(delay)
            except Exception as err:
                retries += 1
                if 'rate limit' in str(err).lower():
                    time.sleep(delay * 2)
                else:
                    raise
        return '\n'.join([f'{result['title']}\n{result['body']}' for result in results])
    except Exception as err:
        return f'Error: {err}'

class SportsStatistics(BaseModel):
    team_name: str = Field(..., description='The name of the NFL team.', example=['New England Patriots'])
    season_year: int = Field(..., description='The year of the season.', example=[2022])

@tool('Sports Statistics Tool', args_schema=SportsStatistics)
def sports_statistics_tool(team_name: str, season_year: int) -> str:
    """
    Retrieves current team statistics and past performance data for NFL teams.
    """
    import requests
    import json
    import os
    api_key = os.environ.get('NFL_API_KEY')
    try:
        url = f'https://api.sportsdata.io/nfl/scores/json/Teams/{team_name}/{season_year}?key={api_key}'
        response = requests.get(url)
        if response.status_code == 404:
            return f'Error: Team {team_name} not found for season {season_year}'
        data = response.json()
        if 'error' in data:
            return f'Error: {data['error']}'
        else:
            return json.dumps(data, indent=4)
    except Exception as err:
        return f'Error: {err}'

class SportsData(BaseModel):
    team_name: str = Field(..., description='The name of the team to fetch data for.', example=['Bengals', 'Ravens'])

@tool('Sports Data Tool', args_schema=SportsData)
def sports_data_tool(team_name: str):
    """
    Fetches the current team statistics and past performance data of the given team from ESPN.
    """
    import requests
    from bs4 import BeautifulSoup
    import os
    api_key = os.environ.get('ESPN_API_KEY')
    try:
        url = f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_name.lower()}'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            team_data = {}
            team_data['team_name'] = data['team']['displayName']
            team_data['wins'] = data['team']['wins']
            team_data['losses'] = data['team']['losses']
            team_data['ties'] = data['team']['ties']
            team_data['past_performance'] = [game['competitions'][0]['competitors'][0]['team']['displayName'] for game in data['team']['schedule']['events']]
            return team_data
        else:
            return {'error': f'Failed to fetch data. Status code: {response.status_code}'}
    except Exception as err:
        return {'error': f'Error: {err}'}

class WeatherForecast(BaseModel):
    city: str = Field(..., description='The city for which the weather forecast is required.', example=['New York'])
    state: str = Field(..., description='The state for which the weather forecast is required.', example=['New York'])
    zip_code: str = Field(..., description='The zip code for which the weather forecast is required.', example=['10001'])

@tool('Weather Forecast Tool', args_schema=WeatherForecast)
def weather_forecast_tool(city: str, state: str, zip_code: str, api_key: str) -> str:
    """
    Retrieves 10-day weather forecasts for a specific location.
    """
    import requests
    import json
    base_url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {'q': f'{city},{state},{zip_code}', 'appid': api_key, 'units': 'imperial'}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        forecast = []
        for i in range(0, 40, 4):
            forecast.append({'date': data['list'][i]['dt_txt'], 'weather': data['list'][i]['weather'][0]['description'], 'temperature': data['list'][i]['main']['temp'], 'humidity': data['list'][i]['main']['humidity']})
        return json.dumps(forecast, indent=4)
    except requests.exceptions.HTTPError as errh:
        return f'HTTP Error: {errh}'
    except requests.exceptions.ConnectionError as errc:
        return f'Error Connecting: {errc}'
    except requests.exceptions.Timeout as errt:
        return f'Timeout Error: {errt}'
    except requests.exceptions.RequestException as err:
        return f'Something went wrong: {err}'

class Location(BaseModel):
    location: str = Field(..., description='The location to fetch the weather data for.', example=['London'])

class AlternativeWeatherFetcher(BaseModel):
    city: str = Field(..., description='The city to fetch weather data for.', example=['Macon'])
    state: str = Field(..., description='The state to fetch weather data for.', example=['GA'])

@tool('Alternative Weather Fetcher Tool', args_schema=AlternativeWeatherFetcher)
def alternative_weather_fetcher_tool(city: str, state: str) -> str:
    """
    Fetches the current weather data for the given city and state using the OpenWeatherMap API.
    """
    import requests
    import os
    import json
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    try:
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': f'{city},{state}', 'appid': api_key, 'units': 'imperial'}
        response = requests.get(base_url, params=params)
        weather_data = response.json()
        return json.dumps(weather_data, indent=4)
    except Exception as err:
        return f'Error: {err}'

class AlternativeWeatherFetcher(BaseModel):
    city: str = Field(..., description='The city to fetch weather data for.', example=['Macon'])
    state: str = Field(..., description='The state to fetch weather data for.', example=['GA'])

class RandomNumberGenerator(BaseModel):
    min_value:int=Field(...,description="The minimum value for the random numbers.",example=[1])
    max_value:int=Field(...,description="The maximum value for the random numbers.",example=[49])
    count:int=Field(...,description="The number of unique random numbers to generate.",example=[6])

@tool("Random Number Generator Tool",args_schema=RandomNumberGenerator)
def random_number_generator_tool(min_value:int,max_value:int,count:int)->str:
    """
    Generates a specified number of unique random numbers within a given range.
    """
    import random
    try:
        if min_value >= max_value:
            return "Error: min_value should be less than max_value"
        if count > max_value - min_value + 1:
            return "Error: count should not be more than the range of numbers"
        random_numbers=random.sample(range(min_value,max_value+1),count)
        return ','.join(map(str,random_numbers))
    except Exception as err:
        return f"Error: {err}"

