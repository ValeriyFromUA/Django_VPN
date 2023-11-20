from urllib.parse import urlparse


def get_domain_from_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain:
        return f"https://{domain}"


def modify_links(soup, domain):
    excluded_extensions = ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.php']
    body = soup.find('body')
    if body:
        for a_tag in body.find_all('a', href=True):
            link = a_tag['href']
            if not any(char in link for char in excluded_extensions):
                links_with_domain = get_domain_from_url(link)
                if links_with_domain:
                    if domain == links_with_domain:
                        modified_link = f'/portal/https://{link}'.replace('https://https://', 'https://')
                        a_tag['href'] = modified_link
                if domain not in link and not any(char in link for char in excluded_extensions):
                    modified_link = f'/portal/https://{domain}/{link}'.replace('https://https://', 'https://')
                    a_tag['href'] = modified_link
