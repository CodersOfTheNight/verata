import click
import yaml

from dotenv import load_dotenv, find_dotenv


@click.command()
@click.option("--env", default=find_dotenv())
@click.option("--config")
def main(env, config):
    load_dotenv(env)
    with open(config, "r") as f:
        cfg = yaml.load(f)


if __name__ == "__main__":
    main()
