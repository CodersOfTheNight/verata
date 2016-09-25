import click
import logging

from dotenv import load_dotenv, find_dotenv
from grazer.config import Config
from grazer.core import crawler


@click.command()
@click.option("--env", default=find_dotenv())
@click.option("--config")
@click.option("--log_level", default="INFO")
def main(env, config, log_level):
    logging.basicConfig(level=getattr(logging, log_level))
    load_dotenv(env)
    cfg = Config(config)
    for record, link in crawler.create(cfg):
        print(record)

if __name__ == "__main__":
    main()
