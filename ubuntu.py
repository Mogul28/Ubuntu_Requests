import os
import requests
from urllib.parse import urlparse

def download_image(url):
    """
    Downloads an image from a URL, saves it to a 'Fetched_Images' directory,
    and handles potential errors.
    """
    try:
        # Step 1: Prompt the user for a URL
        print("Connecting to the web community...")

        # Step 2: Create a directory called "Fetched_Images" if it doesn't exist
        # Principle: Sharing - organize the fetched images for later sharing
        dir_name = "Fetched_Images"
        os.makedirs(dir_name, exist_ok=True)
        print(f"Ensured directory '{dir_name}' exists.")

        # Step 3: Fetch the image from the provided URL using requests
        # Principle: Community - connect to the wider web community
        response = requests.get(url, stream=True)
        
        # Step 4: Check for HTTP errors
        # Principle: Respect - handle errors gracefully
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

        # Step 5: Extract the filename from the URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If the filename is empty (e.g., URL ends in a slash), generate a default name
        if not filename:
            filename = f"image_{os.path.basename(url).split('/')[-1]}.jpg" if os.path.basename(url) else "default_image.jpg"
            print(f"No filename found in URL. Using generated name: {filename}")
        
        # Ensure the filename is appropriate
        if '.' not in filename:
            filename += '.jpg' # Simple fallback for cases where extension is missing

        save_path = os.path.join(dir_name, filename)

        # Step 6: Save the image in binary mode
        # Principle: Practicality - create a tool that serves a real need
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Success! Image downloaded and saved as '{save_path}'")

    except requests.exceptions.HTTPError as err_h:
        print(f"HTTP Error occurred: {err_h}")
        print("Could not fetch the image. The URL might be invalid or the image is not available.")
    except requests.exceptions.ConnectionError as err_c:
        print(f"Connection Error occurred: {err_c}")
        print("Failed to connect to the server. Please check your internet connection or the URL.")
    except requests.exceptions.Timeout as err_t:
        print(f"Timeout Error occurred: {err_t}")
        print("The request timed out. The server might be slow or not responding.")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    image_url = input("Enter the URL of the image you want to download: ")
    if image_url:
        download_image(image_url)
    else:
        print("No URL was entered. Exiting.")