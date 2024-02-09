import requests
from bs4 import BeautifulSoup
import json

def scrape_cnn_world():
    url = 'https://edition.cnn.com/world'
    articles = []

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Assuming CNN articles can be found within <h3> tags or another consistent pattern
        # Note: The actual class names and tags will likely differ and need to be adjusted
        article_elements = soup.find_all('div', class_='card container__item container__item--type-media-image container__item--type-section container_lead-plus-headlines__item container_lead-plus-headlines__item--type-section')
        
        for element in article_elements:
            title = element.text.strip()
            # Ensure the link is absolute; CNN often uses absolute URLs, but check and adjust if needed
            link = element.find('a', href=True)
            if link:
                link = link['href']
                # CNN links might be relative to the domain
                if not link.startswith('http'):
                    link = f'https://edition.cnn.com{link}'

                articles.append({
                    'title': title,
                    'link': link
                })
    
    return articles

if __name__ == '__main__':
    articles = scrape_cnn_world()
    with open('cnn_articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
