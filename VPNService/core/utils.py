from urllib.parse import urlparse


def get_domain_from_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain:
        return f"https://{domain}"


def modify_links(soup, domain):
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']

        links_with_domain = get_domain_from_url(link)
        if links_with_domain:
            if domain == links_with_domain:
                modified_link = f'/vpn/proxy_more/https://{link}'.replace('https://https://', 'https://')
                print('1_______', modified_link)
                a_tag['href'] = modified_link
        if domain not in link:
            print(link)
            modified_link = f'/vpn/proxy_more/https://{domain}/{link}'.replace('https://https://', 'https://')
            print('2_______', modified_link)

            a_tag['href'] = modified_link
