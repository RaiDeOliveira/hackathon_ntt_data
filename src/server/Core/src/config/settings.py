import yaml

def load_config():
    try:
        with open("config.yml", "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise Exception("config.yml file not found.")
    except yaml.YAMLError as exc:
        raise Exception(f"Error parsing config.yml: {exc}")

config = load_config()
