import json
import argparse


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return ''.join(i.capitalize() for i in s[0:])


def print_ident(f, indent, text):
    f.write("{}{}\n".format("    " * indent, text))


def print_ident_str(indent, text):
    return "{}{}\n".format("    " * indent, text)


def describe_class(file,
                   class_data: dict,
                   class_name: str = "Main",
                   indent=1,
                   prop=False,
                   comments=False,
                   default=False):
    class_descriptrion = ""
    class_descriptrion += print_ident_str(indent - 1, "@dataclass")
    class_descriptrion += print_ident_str(indent - 1,
                                          "class {}:".format(class_name))

    subclasses = dict()

    for key, value in sorted(class_data.items()):
        if value is None:
            class_descriptrion += print_ident_str(
                indent, "#{}: {} = None".format(key,
                                                type(value).__name__))
        else:
            if isinstance(value, dict):
                class_name_new = to_camel_case(str(key))
                subclasses[key] = (class_name_new, value, False)
                class_descriptrion += print_ident_str(
                    indent, "{}_: {}  = None".format(key, class_name_new))

            elif isinstance(value, list):
                if len(value) == 0:
                    continue

                item = value[0]
                if isinstance(item, dict):

                    class_name_new = to_camel_case(str(key))
                    subclasses[key] = (class_name_new, item, True)
                    class_descriptrion += print_ident_str(
                        indent,
                        "{}: List[{}]  = None".format(key, class_name_new))

                else:
                    class_descriptrion += print_ident_str(
                        indent,
                        "{}: {}  = None".format(key,
                                                type(value).__name__))

            else:
                class_descriptrion += print_ident_str(
                    indent, "{}: {}  = None".format(key,
                                                    type(value).__name__))

    if default is True:
        class_descriptrion += print_ident_str(0, "")
        class_descriptrion += print_ident_str(indent, "@classmethod")
        class_descriptrion += print_ident_str(indent, "def __default__(cls):")
        if comments is True:
            class_descriptrion += print_ident_str(indent + 1,
                                                  "# {}".format(class_data))
        class_descriptrion += print_ident_str(indent + 1, "obj = cls()")
        for key, value in class_data.items():
            if isinstance(value, dict):
                class_descriptrion += print_ident_str(
                    indent + 1, "obj.{} = {}.__default__()".format(
                        key, to_camel_case(str(key))))
            elif isinstance(value, str):
                class_descriptrion += print_ident_str(
                    indent + 1, "obj.{} = \"{}\"".format(key, value))
            else:
                class_descriptrion += print_ident_str(
                    indent + 1, "obj.{} = {}".format(key, value))
        class_descriptrion += print_ident_str(indent + 1, "return obj")

    class_descriptrion += print_ident_str(0, "")
    class_descriptrion += print_ident_str(indent,
                                          "def __init__(self, data: dict):")
    class_descriptrion += print_ident_str(indent + 1, "self.__dict__ = data")
    for key, value in sorted(subclasses.items()):
        if value[2] == False:
            class_descriptrion += print_ident_str(
                indent + 1,
                'self.{} = None if data.get("{}", None) is None else {}(data["{}"])'
                .format(key, key, value[0], key))
        else:
            class_descriptrion += print_ident_str(
                indent + 1,
                'self.{} = None if data.get("{}", None) is None else list( map(lambda x: {}(x), data["{}"]))'
                .format(key, key, value[0], key))

    if prop is True:
        class_descriptrion += print_ident_str(0, "")
        for key, value in sorted(subclasses.items()):
            class_descriptrion += print_ident_str(indent, "@property")
            class_descriptrion += print_ident_str(indent,
                                                  "def {}(self,):").format(key)
            class_descriptrion += print_ident_str(
                indent + 1, "return self.{}.__dict__".format(key))

    # print_ident(file, 0, "")
    for key, value in sorted(subclasses.items()):
        describe_class(file,
                       value[1],
                       value[0],
                       indent,
                       prop=prop,
                       comments=comments,
                       default=default)

    print_ident(file, 0, class_descriptrion)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Json parser into Python Dataclass.')

    parser.add_argument('-f',
                        '--file',
                        metavar="",
                        help='input file with json',
                        required=True)

    parser.add_argument('-o',
                        '--output',
                        metavar="",
                        help='file to store result',
                        default="result.class.py",
                        required=False)
    parser.add_argument(
        '--with-property',
        dest='property',
        action='store_true',
        help='add property for inner classes (for serializtion)')
    parser.add_argument('--with-comments',
                        dest='comments',
                        action='store_true',
                        help='add comments')
    parser.add_argument('--with-default',
                        dest='default',
                        action='store_true',
                        help='add classmethod default to generate object')
    parser.set_defaults(property=False)
    parser.set_defaults(comments=False)
    parser.set_defaults(default=False)

    args = parser.parse_args()

    # Prepare all
    l = open(args.file, "r").read()
    while (l.find("\"{") != -1):
        l = l[:l.find("\"{")] + "null" + l[l.find("}\"") + 2:]
    f = open(args.output, 'w')
    res = json.loads(l)

    describe_class(f,
                   res,
                   prop=args.property,
                   comments=args.comments,
                   default=args.default)
