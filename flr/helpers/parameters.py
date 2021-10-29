import yaml
import argparse
import pathlib


def load_yml(filepath: str):
    p = pathlib.Path(filepath)

    if p.exists() is False:
        raise FileNotFoundError()
    with p.open() as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def parse_args():
    x = argparse.ArgumentParser()
    x.add_argument('--debug', '-d', help="extra logging", action='store_true')
    x.add_argument('--config', '-c', help="Path to config.yml")
    x.add_argument('--creds', '-u', help="Path to creds file")
    x.add_argument('--notimeout', help="Dont use timeout in prod", action="store_true")
    x.add_argument("--dev", help="Enable development mode", action="store_true")
    x.add_argument("--timeout", "-t", help="Time (minutes) to run the program for")
    return x.parse_args()