import re
import logging

from functools import wraps

logger = logging.getLogger("Parsing")


def create_node(data):
    tag_part = r"(?P<tag>\w+)"
    attr_part = r"(?P<q>\[(?P<attr>\w+)=(\"|\')(?P<val>.+?)(\"|\')\])?"
    selector_part = r"(\{(?P<selector>\d+)\})?"
    attr_selector_part = r"(?P<as>\.(\w|[_])+)?"
    p = tag_part + attr_part + selector_part + attr_selector_part
    patt = re.compile(p)

    m = patt.match(data)
    tag = m.group("tag")

    if m.group("q"):
        q = {m.group("attr"): m.group("val")}
    else:
        q = None

    def selector(lst):
        s = m.group("selector")
        if s:
            sel = int(s)
            return [lst[sel]] if sel < len(lst) else []
        else:
            return lst

    def attr_selector(lst):
        f = m.group("as")
        if f:
            return [item[f] for item in lst]
        else:
            return lst

    @wraps("Path: {0}".format(data))
    def node(root):
        return selector(root.findAll(tag, q))

    node.__name__ = data

    return node


def parse(key, paths, context):
    path = paths.popleft()
    results = []

    for node in context:
        for out in path(node):
            results.append(out)

    logger.debug("Context {0} after {1}".format(results, path.__name__))
    if len(paths) == 0:
        # End of line
        return [(key, result.text, result.attrs)
                for result in results]
    else:
        return parse(key, paths, results)
