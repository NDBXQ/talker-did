import yaml  

def load_yaml_config(config_file="config.yaml"):
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            return config