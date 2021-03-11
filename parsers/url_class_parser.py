from collections import OrderedDict

l = "submodel=Mi%20A2&android_app_volume=1&disable_ml=false&format=320x50_mb&is_nonagon=true&android_app_muted=false&am=0&dv=0&gl=US&hl=en&js=afma-sdk-a-v204102000.204102000.0&lv=204102000&ms=CoACGyxxslBU6LPISYnwnOZw3QmUFWmPxfGZ6897FRdHg8xJtfj1qETI4Vw9bmzJyvjGdvyNs8Vu71XUGB59WvhDK4LnQgjsX69yHS4eZp6zbDtPpR8RZDfo3TOQ11pAQcOsM2V-cKFqnsEK68Ku8QhmuWuiNAWvPOJIiOE7x9jcXlvNUYaS_KHmxYaiTZUpjkQQ7je_WbmFPBy1vBVZoQIi6n484MRtOoMXfcs4ZmnTNeXGn1QscbvVQHhwcH_JtBV-bqoqu4m1OoeZL__gysrfCuNi8E1mZu8-aSqSrKqEP0KW2ZDavtu85byAUulBT-lnDrCpT_6Vd6jPpDPKzYMwDAqAAjo1pMtsDv4f3QAoX30xo4arJAy8xM3RbbHMKfGYpF1QGKvIfQWWhf4vGA1HJink3PZEVhXYoqRE3xz3nhEYlIOk0DmGU8BYHYQ9Ze5VEDdl7bGH2_AB-tS0BYET-tS7rGjp5ubcKlXTw8IBP2LWWH8kLkpulaAD4137SppKyZwve5LHC7OvhE8pfuzvRbkvjk45I6vglM3xF68Asf_9dtA8edKcVNSOOp1iJzFg_PQNEDQDYREIIR-nktnXNmZ9SR47mEdkufoRdNKiJ8TzDLSbjcZYirgOzhV7-QHk6gipGkBpWgj-q9UWv7WmjDOaT-28Ul6taINDPOHxNXwxCoUSEEegszyFqSF9XUBp-QZ2QIc&rm=0&sp=false&coh=true&riv=0&u_sd=2.75&request_id=d6cc4c43-5498-4324-89a2-9dbae3a08b93&render_in_browser=false&target_api=30&carrier=25701&app_open_version=2&is_sidewinder=false&seq_num=24&_c_csdk_npa_o=false&guci=0.0.0.0.0.0.0.0&cap=ma&u_w=393&u_h=738&msid=com.tzz.superapp&an=1.android.com.tzz.superapp&_package_name=com.tzz.superapp&app_name=1.android.com.tzz.superapp&net=wi&u_audio=3&u_so=p&loeid=44738144&preqs_in_session=23&support_transparent_background=true&preqs=23&time_in_session=1418360&output=html&region=mobile_app&u_tz=180&client_sdk=1&ex=1&client=ca-app-pub-3970137583594976&slotname=6355384505&gsb=wi&ogsb=wi&lite=0&caps=inlineVideo_interactiveVideo_mraid1_mraid2_mraid3_sdkVideo_th_autoplay_mediation_scroll_av_av_transparentBackground_sdkAdmobApiForAds_di_sfv_dinm_dim_nav_navc_dinmo_ipdof_gls_xSeconds&bisch=true&blev=1&swdr=false&cans=5&canm=false&heap_free=17932848&heap_max=268435456&heap_total=28568016&wv_count=2&blockAutoClicks=true&rewarded_version=2&includeDoritos=true&includeCookies=true&session_idl=-1&blob=ABPQqLGoDDtXDcMynNVJfB6rSRFsmYwKmlemDaaj4S58lh6f1itb_4tnM837iOTs2itix6iK8xXjGGO608NZ-50RGqx4sOyZ7qy9lwstzaJpBdOFZp9fGH0qptEHtBOwgLkYG93fQI8EitQio85jQ3ZXMI4-8EVf01PqLHME0bpkcJnUGwBwutoExfUpFZRCteaXE7QviIridFYjRLsnumZ2zgbY2UOu4vK4Em8oGiFUJ0fCylZ761veOrxpCA&et=8&tcar=15&jsv=sdk_20190107_RC02-production-sdk_20210305_RC00&urll=2305"

def parse_url_to_dict(url: str):
    """! Url params to dict. """
    result = OrderedDict()
    for value in url.split('&'):
        value = value.split('=')
        result[value[0]] = value[1]
        result.move_to_end(value[0])

    return result

def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return ''.join(i.capitalize() for i in s[0:])


def print_ident(f, indent, text):
    f.write("{}{}\n".format("    " * indent, text))


def url_type(value: str):
    try:
        new_value = int(value)
        return int
    except Exception as _:
        return str

def describe_class(file, class_data: dict, class_name: str = "Main", indent=1):
    print_ident(file, indent - 1, "@dataclass")
    print_ident(file, indent - 1, "class {}:".format(class_name))

    subclasses = dict()

    for key, value in class_data.items():
        if value is None:
            print_ident(file, indent,
                        "#{}: {} = None".format(key,
                                                url_type(value).__name__))
        else:
            if isinstance(value, dict):
                class_name_new = to_camel_case(str(key))
                subclasses[key] = (class_name_new, value, False)
                print_ident(file, indent,
                            "{}: {}  = None".format(key, class_name_new))

            elif isinstance(value, list):
                if len(value) == 0:
                    continue

                item = value[0]
                if isinstance(item, dict):

                    class_name_new = to_camel_case(str(key))
                    subclasses[key] = (class_name_new, item, True)
                    print_ident(
                        file, indent,
                        "{}: List[{}]  = None".format(key, class_name_new))

                else:
                    print_ident(
                        file, indent,
                        "{}: {}  = None".format(key,
                                                url_type(value).__name__))

            else:
                print_ident(file, indent,
                            "{}: {}  = None".format(key,
                                                    url_type(value).__name__))

    ## Add `__init__` function
    print_ident(file, 0, "")
    print_ident(file, indent, "def __init__(self, data: dict = None):")
    print_ident(file, indent + 1, "if data is not None:")
    print_ident(file, indent + 2, "self.__dict__ = data")

    for key, value in sorted(subclasses.items()):
        if value[2] == False:
            print_ident(
                file, indent + 1,
                'self.{} = None if data.get("{}", None) is None else {}(data["{}"])'
                .format(key, key, value[0], key))
        else:
            print_ident(
                file, indent + 1,
                'self.{} = None if data.get("{}", None) is None else list( map(lambda x: {}(x), data["{}"]))'
                .format(key, key, value[0], key))

    ## Add `__default__` function
    print_ident(file, 0, "")
    print_ident(file, indent, "@classmethod")
    print_ident(file, indent, "def __default__(cls):")
    print_ident(file, indent + 1, "obj = cls()")
    for key, value in class_data.items():
        print_ident(file, indent + 1, "obj.{} = {}".format(key, value if url_type(value) == int else '\"{}\"'.format(value)))
    print_ident(file, indent + 1, "return obj")


    ## Add `to_url` function
    print_ident(file, 0, "")
    print_ident(file, indent, "def to_url(self) -> str:")
    print_ident(file, indent + 1, "url = str()")
    # for key, value in class_data.items():
    #     print_ident(file, indent + 1, "obj.{} = {}".format(key, value if url_type(value) == int else '\"{}\"'.format(value)))
    print_ident(file, indent + 1, "url = \"&\".join(map(lambda x: '{}={}'.format(x[0], x[1]), self.__dict__.items()))")
    print_ident(file, indent + 1, "return url")

    print_ident(file, 0, "")
    for key, value in sorted(subclasses.items()):
        describe_class(file, value[1], value[0], indent)


f = open("result.class.py", 'w')
res = parse_url_to_dict(l)
print(res.items())

describe_class(f, res)