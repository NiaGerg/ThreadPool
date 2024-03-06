import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import json
import time


def fetch_product(url):
    response = requests.get(url)
    try:
        product_data = response.json()
        return product_data
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def thread_worker(product_urls):
    with ThreadPoolExecutor(max_workers=20) as thread_executor:
        futures = [thread_executor.submit(fetch_product, url) for url in product_urls]

        products_data = []
        for future in futures:
            product_data = future.result()
            if product_data is not None:
                products_data.append(product_data)

    return products_data


def process_worker(process_id, product_urls):
    products_data = []
    for i in range(process_id * 5, (process_id + 1) * 5):
        product_data = fetch_product(product_urls[i])
        if product_data is not None:
            products_data.append(product_data)

    return products_data


def main():
    url = "https://dummyjson.com/products/"
    num_products = 100

    product_urls = [f"{url}{i}" for i in range(1, num_products + 1)]

    thread_futures = []
    with ThreadPoolExecutor(max_workers=5) as thread_executor:
        for _ in range(5):
            future = thread_executor.submit(thread_worker, product_urls)
            thread_futures.append(future)

    process_futures = []
    with ProcessPoolExecutor(max_workers=5) as process_executor:
        for i in range(5):
            future = process_executor.submit(process_worker, i, product_urls)
            process_futures.append(future)

    products_data = []

    for future in thread_futures:
        products_data.extend(future.result())

    for future in process_futures:
        products_data.extend(future.result())

    with open("products.json", "w") as json_file:
        json.dump(products_data, json_file, indent=2)


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    time = end_time - start_time
    print(f"Execution time: {time} seconds")
