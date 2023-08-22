from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/numbers', methods=['GET'])
def get_numbers():
    url_params = request.args.getlist('url')

    def fetch_numbers_from_url(url):
        try:
            response = requests.get(url, timeout=0.5)
            if response.status_code == 200:
                return response.json().get('numbers', [])
        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            print(f"Error fetching numbers from {url}: {e}")
        return []

    all_numbers = []
    for url in url_params:
        numbers = fetch_numbers_from_url(url)
        all_numbers.extend(numbers)

    return jsonify(numbers=all_numbers)

if __name__ == '__main__':
    app.run(debug=True, port=3000)