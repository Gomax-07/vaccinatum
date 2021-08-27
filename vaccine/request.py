from vaccine import vaccine
import urllib.request,json
from .api import covid

Covid =covid.Covid


# Getting the covid base url
base_url = vaccine.config["REQUEST_BASE_URL"]

def get_cases(category):
    '''
    Function that gets the json response to our url request
    '''
    base_url = base_url.format(category)

    with urllib.request.urlopen(base_url) as url:
        get_covid_data = url.read()
        get_covid_response = json.loads(get_covid_data)

        covid_results = None

        if get_covid_response['results']:
            covid_results_list = get_covid_response['results']
            covid_results = process_results(covid_results_list)


    return covid_results

def process_results(covid_list):
    '''
    Function  that processes the covid result and transform them to a list of Objects

    Args:
        covid_list: A list of dictionaries that contain covid details

    Returns :
        covid_results: A list of movie objects
    '''
    covid_results = []
    for covid_item in covid_list:
        id = covid_item.get('id')
        iso3 = iso3_item.get('iso3')
        cases = cases_item.get('cases')
        deaths = deaths_item.get('deaths')
        recovered = recoverd_item.get('recovered')
        

        if poster:
            movie_object = Movie(id,iso3,cases,deaths,recovered)
            movie_results.append(movie_object)

    return covid_results