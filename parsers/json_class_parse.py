import json

l = open("file.json", "r").read()

while (l.find("\"{") != -1):
    l = l[:l.find("\"{")] + "null" + l[l.find("}\"") + 2:]


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return ''.join(i.capitalize() for i in s[0:])


def print_ident(f, indent, text):
    f.write("{}{}\n".format("    " * indent, text))


def describe_class(file, class_data: dict, class_name: str = "Main", indent=1):
    print_ident(file, indent - 1, "@dataclass")
    print_ident(file, indent - 1, "class {}:".format(class_name))

    subclasses = dict()

    for key, value in sorted(class_data.items()):
        if value is None:
            print_ident(file, indent, "#{}: {} = None".format(key, type(value).__name__))
        else:
            if isinstance(value, dict):
                class_name_new = to_camel_case(str(key))
                subclasses[key] = (class_name_new, value, False)
                print_ident(file, indent, "{}: {}  = None".format(key, class_name_new))

            elif isinstance(value, list):
                if len(value) == 0:
                    continue

                item = value[0]
                if isinstance(item, dict):

                    class_name_new = to_camel_case(str(key))
                    subclasses[key] = (class_name_new, item, True)
                    print_ident(file, indent, "{}: List[{}]  = None".format(key, class_name_new))

                else:
                    print_ident(file, indent, "{}: {}  = None".format(key, type(value).__name__))

            else:
                print_ident(file, indent, "{}: {}  = None".format(key, type(value).__name__))

    print_ident(file, 0, "")
    print_ident(file, indent, "def __init__(self, data: dict):")
    print_ident(file, indent + 1, "self.__dict__ = data")

    for key, value in sorted(subclasses.items()):
        if value[2] == False:
            print_ident(
                file,
                indent + 1,
                'self.{} = None if data.get("{}", None) is None else {}(data["{}"])'.format(
                    key, key, value[0], key))
        else:
            print_ident(
                file,
                indent + 1,
                'self.{} = None if data.get("{}", None) is None else list( map(lambda x: {}(x), data["{}"]))'
                .format(key, key, value[0], key))

    print_ident(file, 0, "")
    for key, value in sorted(subclasses.items()):
        describe_class(file, value[1], value[0], indent)


f = open("result.class.py", 'w')
res = json.loads(l)

describe_class(f, res)