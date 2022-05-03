from .bounds import Bounds

def bounds_type(strings):
    import argparse
    strings = strings.replace("(", "").replace(")", "")
    floats = tuple(map(float, strings.split(",")))
    if len(floats) == 4:
        floats.append( 20.0 ) # add a default read resolution to the end
    try:
        b = Bounds(*floats)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"{e}")
    return b


def get_parser(args):

    import argparse

    parser = argparse.ArgumentParser(description='Apply a PDAL pipeline over a COPC file to construct an elevation model')
    parser.add_argument('copc_file',
                        help='COPC file to process')
    parser.add_argument('--threshold',
                        help='How many points before we split?', type =int, default=500000)
    parser.add_argument('--read_resolution',
                        help='Reading resolution threshold', type =float, default=20.0)
    parser.add_argument('--write_resolution',
                        help='Raster output resolution', type =float, default=20.0)
    parser.add_argument('--collar',
                        help='Distance of read collar/buffer', type =float, default=10.0)
    parser.add_argument('--output_dir',
                        help='Output directory', type =str, default='dtm')
    parser.add_argument('--dimension',
                        help='Dimension name to write', type =str, default='Z')
    parser.add_argument('--output_type',
                        help='Output type, ie idw, max, min, etc', type =str, default='idw')
    parser.add_argument('--window_size',
                        help='writers.gdal window_size', type =int, default=3)
    parser.add_argument('--bounds',
                        help='Limiting bounds', type =bounds_type, default=None)
    parser.add_argument('--debug',
                        action='store_true',
                        help='print debug messages to stderr')


    args = parser.parse_args(args)
    return args
