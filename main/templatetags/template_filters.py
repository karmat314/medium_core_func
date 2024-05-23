# myapp/templatetags/custom_filters.py
from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter(name='strip_images')
def strip_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove all img tags
    for img in soup.find_all('img'):
        img.decompose()
    
    # Get text only
    text = soup.get_text()
    return text



