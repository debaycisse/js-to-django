from django.conf import settings
from os import path, makedirs
from PIL import Image, ImageDraw
from .models import Country
from .serializers import CountrySerializer

def generate_image():
    '''
    generates a statistics image for the countries
    '''

    # create image and specify the directory to store it
    output_directory = settings.MEDIA_ROOT
    makedirs(output_directory, exist_ok=True)

    _image = Image.new('RGB', (600, 400), color=(85, 46, 8))
    _canvas = ImageDraw.Draw(_image)

    # construct the texts to make up the image contents (texts)
    total_countries = get_country_counts()
    top_five = get_top_five_by_estimate()
    last_refreshed_at = get_last_refreshed_at()

    _texts = [
        f'Total number of countries : {total_countries}',
        f'Top 5 countries by estimated GDP :',
        f'1. {top_five[0]}',
        f'2. {top_five[1]}',
        f'3. {top_five[2]}',
        f'4. {top_five[3]}',
        f'5. {top_five[4]}',
        f'Time stamp of the last refresh : {last_refreshed_at}'
    ]

    x_axis = 30
    y_axis = 30
    line_space = 40

    for line in _texts:
        _canvas.text((x_axis, y_axis), line, fill=(255, 255, 204))
        if any([
            'Top 5 countries ' in line,
            '1. ' in line,
            '2. ' in line,
            '3. ' in line,
            '4. ' in line,
        ]):
            y_axis += 20
        else:
            y_axis += line_space

    output_path = path.join(output_directory, 'summary.png')
    
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

    top_five = [country.get('name') for country in serializer.data]

    return top_five

def get_country_counts():
    '''
    obtains the total number of countries

    Returns:
        the total count of all countries
    '''
    counts = Country.objects.count()

    return counts 

def get_last_refreshed_at():
    '''
    obtains the latest refreshed_at's time and date
    '''

    queryset = Country.objects.all().order_by('-last_refreshed_at').first()

    return queryset.last_refreshed_at.strftime('%Y-%m-%dT%H:%M:%SZ')
