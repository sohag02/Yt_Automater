import requests
import threading
import logging

logger = logging.getLogger(__name__)

def verify_proxy(proxy, output_path):
    url = "https://www.youtube.com"
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        response.raise_for_status()
        with open(output_path, "a") as outfile:
            outfile.write(proxy + "\n")
        logging.debug(f"Working proxy: {proxy}")
    except requests.exceptions.RequestException:
        logging.debug(f"Failed proxy: {proxy}")

def check_proxies(file_path, output_path="working_proxies.txt"):
    logging.info("Checking Proxies...")
    with open(file_path, "r") as file:
        proxies = [line.strip() for line in file.readlines()]
    
    threads = []

    for proxy in proxies:
        thread = threading.Thread(target=verify_proxy, args=(proxy, output_path))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logging.info(f"Successfully saved working proxies in {output_path}")

def get_proxy(file="working_proxies.txt"):
    # get a proxy and delete it from the file
    with open(file, "r") as f:
        proxies = f.readlines()

    proxy = proxies[0].strip()
    with open(file, "w") as f:
        f.writelines(proxies[1:])

    return proxy

if __name__ == "__main__":
    input_file = "proxies.txt"  # Replace with the path to your proxy list file
    output_file = "working_proxies.txt"  # File where working proxies will be saved
    check_proxies(input_file, output_file)
