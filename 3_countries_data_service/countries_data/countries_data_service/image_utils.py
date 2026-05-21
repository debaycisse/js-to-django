from os import getenv, path, makedirs
from PIL import Image, ImageDraw
from .models import Country
from .serializers import CountrySerializer

def generate_image():
    '''
    generates a statistics image for the countries
    '''

    # overwrites the image
    output_directory = 'cache'
    output_path = path.join(output_directory, 'summary.png')

    makedirs(output_directory, exist_ok=True)

    _image = Image.new('RGB', (600, 400), color=(0, 0, 128))

    _canvas = ImageDraw.Draw(_image)

    # construct the texts to make up the image contents (texts)
    total_countries = get_country_counts()
    top_five = get_top_five_by_estimate()
    last_refreshed_at = get_last_refreshed_at()

    _texts = [
        f'Total number of countries : {total_countries}',
        f'Top 5 countries by estimated GDP : {top_five}',
        f'Timestamp of last refresh : {last_refreshed_at}'
    ]

    x_axis = 50
    y_axis = 350
    line_space = 70

    for line in _texts:
        _canvas.text((x_axis, y_axis), line, fill=(255, 255, 204))
        y_axis -= line_space
    
    _image.save(output_path)

def get_top_five_by_estimate():
    '''
    obtains and the returns the top five
    countries, based on their gdp

    Returns:
        the top five countries
    '''
    
    qset = Country.objects.order_by('-estimated_gdp')[:5]
    serializer = CountrySerializer(qset, many=True)

    top_five = [country.name for country in serializer.data]
    
    return ', '.join(top_five)

def get_country_counts():
    '''
    obtains the total number of countries

    Returns:
        the total count of all countries
    '''

    return Country.objects.count()

def get_last_refreshed_at():
    '''
    obtains the latest refreshed_at's time and date
    '''

    queryset = Country.objects.order_by('-last_refreshed_at').first()
    serializer = CountrySerializer(queryset)
    return serializer.data.get('last_refreshed_at')
