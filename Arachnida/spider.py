import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL to start crawling from")
    parser.add_argument("-l", type=int, default=5, help="Depth of crawling")
    parser.add_argument("-r", action="store_true", help="Enable recursive crawling")
    parser.add_argument("-p", type=str, default="./data/", help="Path to save images") 

    args = parser.parse_args()  # вот здесь мы получаем результат
    if not args.r and args.l != 5:
        parser.error("Option -l is only valid with -r.")
    return args

def is_valid_url(url):
    # Проверка валидности URL
    return url.startswith("http://") or url.startswith("https://")

def download_page(url):
    # Скачивание страницы
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def crawl(url, depth, max_depth, visited, all_images, start_domain):
    if depth > max_depth or url in visited:
        return

    visited.add(url)
    html = download_page(url)
    if html is None:
        return

    print(f"[{depth}] Crawling: {url}")
    images = extract_image_urls(html, url)
    all_images.update(images)

    if depth < max_depth:
        links = extract_links(html, url, start_domain)
        for link in links:
            crawl(link, depth + 1, max_depth, visited, all_images, start_domain)



# Это функция для нахождения изображений
def extract_image_urls(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    image_urls = []

    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            full_url = urljoin(base_url, src)  # подставляем домен если ссылка относительная
            if full_url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
                image_urls.append(full_url)
    return image_urls

# Это функция для нахождения ссылок на другие страницы 
def extract_links(html, base_url, start_domain):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href:
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            if parsed.scheme in ["http", "https"] and parsed.netloc == start_domain:
                links.append(full_url)
    return links


def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        # Получаем имя файла из URL
        filename = os.path.basename(urlparse(image_url).path)

        # Создаем путь, если его нет
        os.makedirs(save_path, exist_ok=True)

        filepath = os.path.join(save_path, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"[+] Saved image: {filepath}")
    except Exception as e:
        print(f"[!] Failed to download {image_url}: {e}")

def main():
    args = parse_args()
    visited = set()
    all_images = set()
    start_domain = urlparse(args.url).netloc

    if args.r:
        crawl(args.url, 0, args.l, visited, all_images, start_domain)
    else:
        html = download_page(args.url)
        if html:
            all_images.update(extract_image_urls(html, args.url))

    print(f"\nFound {len(all_images)} image(s) total.")
    print(f"Images will be saved in {args.p}")
    for img in all_images:
        download_image(img, args.p)



if __name__ == "__main__":
    main()