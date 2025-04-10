import yaml
import argparse
import requests

# Simulated model for demo purposes
class Orbis1Model:
    def __init__(self, temperature, search_results=None):
        self.temperature = temperature
        self.search_results = search_results

    def generate(self, prompt):
        # You can now use the search results (or the prompt) as context for the generation
        search_context = self.search_results if self.search_results else "No search results found."
        return f"[Orbis1 Output] Prompt: '{prompt}' | Temperature: {self.temperature}\nSearch Context: {search_context}"

def load_config(path="temperature.yaml"):
    # Load temperature from YAML file
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def search_duckduckgo(query):
    # DuckDuckGo search API (using the !bang syntax to get a quick API response)
    url = f"https://duckduckgo.com/html/?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # Or parse the HTML if you need structured data
    else:
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="Prompt to generate text from")
    parser.add_argument("--config", type=str, default="temperature.yaml", help="Path to YAML config file")
    parser.add_argument("--search", action="store_true", help="Enable DuckDuckGo search for the prompt")
    args = parser.parse_args()

    # Load temperature config
    config = load_config(args.config)
    temperature = config.get('temperature', 1.0)  # Default to 1.0 if not specified

    search_results = None
    if args.search:
        # Perform DuckDuckGo search if --search is provided
        search_results = search_duckduckgo(args.prompt)
        if search_results is None:
            print("Failed to fetch search results.")
            search_results = "No search results found."

    # Create the model and generate the response
    model = Orbis1Model(temperature, search_results)
    output = model.generate(args.prompt)
    print(output)

if __name__ == "__main__":
    main()
