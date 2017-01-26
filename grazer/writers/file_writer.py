import logging

logger = logging.getLogger("File Writer")


def write_record(out, record, link):
    logging.debug("Record: {0} Link: {1}".format(record, link))
    out.write("({0}, {1})\n".format(record, link))


def write_result(out, title, info, meta):
    logging.trace("Result: {0}: {1} meta: {2}".format(title, info, meta))
    out.write("{0}, {1}\n".format(title, info))
