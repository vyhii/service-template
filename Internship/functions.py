import numpy as np
def filter_countries(original_countries, country_filter):
    filtered_countries = []
    
    for country in original_countries:
        if country.startswith(country_filter):
            filtered_countries.append(country)

    return(filtered_countries)

def get_first_country(original_countries,):
    return original_countries[0]

def suma(x,y):
    z= x+y
    return z
def division(x,y):
    z = x/y
    return z

if __name__ =='__main__':
    countries =['Australia','United Kingdom','Italy','Spain','France','Sweden','Switzerland']
    filtered_countries = []
    country_filter = "S"
    for country in countries:
        if country.startswith(country_filter):
            filtered_countries.append(country)

    result = filter_countries(countries,"S")
    print(result)

if __name__ =='__main__':
    x = 4
    y = 6
    result = division(x,y)
    print(result)

if __name__ =='__main__':
    countries =['Australia','United Kingdom','Italy','Spain','France','Sweden','Switzerland']
    get_first_country(countries,)
    result = countries[0]
    print(result)