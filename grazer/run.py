import click
import logging
import time

from dotenv import load_dotenv, find_dotenv
from grazer.config import Config
from grazer.core import crawler
from grazer.core import scrapper
from grazer.util import time_convert, grouper

logger = logging.getLogger("Verata")


@click.group()
@click.option("--env", default=find_dotenv(), help="Environment file")
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
@click.option("--config", help="Configuration file", prompt="Enter config")
@click.pass_context
def main(ctx, env, log_level, debug, output, config):
    if output is None:
        logger.error("Please provide output file")
        exit()
    else:
        click.echo(ctx)
        ctx.meta["output"] = output

    ctx.meta["config"] = config

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=getattr(logging, log_level))
    load_dotenv(env)


@main.command()
@click.option("--link", help="Site url for scrapping")
@click.pass_context
def scrape(ctx, link):
    cfg = Config(ctx.meta["config"])
    output = ctx.meta["output"]
    with open(output, "w") as f:
        data = scrapper.fetch_page(link, cfg)
        data = scrapper.scrape(data, cfg.mappings)
        for item in data:
            f.write(item)


@main.command()
@click.option("--paginate",
              help="Split results into pages by",
              default=10,
              type=int)
@click.option("--rest_interval",
              help="How long to wait before fetching next page",
              default="0s")
@click.pass_context
def crawl(ctx, paginate, rest_interval, output):
    rest = time_convert(rest_interval)
    cfg = Config(ctx.meta["config"])
    output = ctx.meta["output"]

    with open(output, "w") as f:
        for chunk in grouper(paginate, crawler.create(cfg)):
            if chunk is None:
                continue

            for record, link in chunk:
                logging.debug("Record: {0} Link: {1}".format(record, link))
                f.write("({0}, {1})\n".format(record, link))

            if rest > 0:
                time.sleep(rest)


if __name__ == "__main__":
    main()
