import re
import logging

logger = logging.getLogger("Parsing")


def create_node(data):
    tag_part = r"(?P<tag>\w+)"
    attr_part = r"(?P<q>\[(?P<attr>\w+)=(\"|\')(?P<val>.+?)(\"|\')\])?"
    selector_part = r"(\{(?P<selector>\d+)\})?"
    p = tag_part + attr_part + selector_part
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

    def node(root):
        return selector(root.findAll(tag, q))

    return node


def parse(key, paths, root):
    context = [root]
    for path in paths:
        node = context.pop()
        logger.debug("Using path: {0} entering context {1}".format(path, node))
        for out in path(node):
            context.append(out)
    return [(key, result.text, result.attrs)
            for result in context]
