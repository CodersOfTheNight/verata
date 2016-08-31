import click

from dotenv import load_dotenv, find_dotenv
from grazer.config import Config


@click.command()
@click.option("--env", default=find_dotenv())
@click.option("--config")
def main(env, config):
    load_dotenv(env)
    cfg = Config(config)

if __name__ == "__main__":
    main()
