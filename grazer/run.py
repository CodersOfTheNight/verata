import click
import logging

from dotenv import load_dotenv, find_dotenv
from grazer.config import Config
from grazer.core import crawler

logger = logging.getLogger("Verata")


@click.command()
@click.option("--env", default=find_dotenv(), help="Environment file")
@click.option("--config", help="Configuration file")
@click.option("--log_level",
              default="INFO",
              help="Defines a log level",
              type=click.Choice(["DEBUG", "INFO", "TRACE"]))
@click.option("--debug",
              default=False,
              is_flag=True,
              help="Shortcut for DEBUG log level")
@click.option("--output", help="All results goes here",
              prompt="Enter output file name")
def main(env, config, log_level, debug, output):
    if output is None:
        logger.error("Please provide output file")
        exit()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=getattr(logging, log_level))
    load_dotenv(env)
    cfg = Config(config)

    with open(output, "w") as f:
        for record, link in crawler.create(cfg):
            logging.debug("Record: {0} Link: {1}".format(record, link))
            f.write("({0}, {1})\n".format(record, link))


if __name__ == "__main__":
    main()
