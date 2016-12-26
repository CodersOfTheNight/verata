import click
import logging
import time

from dotenv import load_dotenv, find_dotenv
from grazer.config import Config
from grazer.core import crawler
from grazer.util import time_convert, grouper

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
@click.option("--paginate",
              help="Split results into pages by",
              default=10,
              type=int)
@click.option("--rest_interval",
              help="How long to wait before fetching next page",
              default="0s")
def main(env, config, log_level, debug, output, paginate, rest_interval):
    if output is None:
        logger.error("Please provide output file")
        exit()

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=getattr(logging, log_level))
    load_dotenv(env)
    cfg = Config(config)
    rest = time_convert(rest_interval)

    with open(output, "w") as f:
        for chunk in grouper(paginate, crawler.create(cfg)):
            for record, link in chunk:
                logging.debug("Record: {0} Link: {1}".format(record, link))
                f.write("({0}, {1})\n".format(record, link))

            if rest > 0:
                time.sleep(rest)


if __name__ == "__main__":
    main()
