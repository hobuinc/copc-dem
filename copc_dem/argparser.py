
def get_parser(args):

    import argparse

    parser = argparse.ArgumentParser(description='Apply a PDAL pipeline over a COPC file to construct an elevation model')
    parser.add_argument('copc_file',
                        help='COPC file to process')
    parser.add_argument('-threshold',
                        help='Point count split threshold', type =int, default=500000)
    parser.add_argument('-read_resolution',
                        help='Point resolution to read data', type =float, default=20.0)
    parser.add_argument('-write_resolution',
                        help='Raster resolution to write data', type =float, default=20.0)
    parser.add_argument('-collar',
                        help='Raster resolution to write data', type =float, default=10.0)
    parser.add_argument('-output_dir',
                        help='Output directory', type =str, default='dtm')
    parser.add_argument('-output_type',
                        help='Output type', type =str, default='idw')
    parser.add_argument('-window_size',
                        help='Output type', type =int, default=3)
    parser.add_argument('--debug',
                        action='store_true',
                        help='print debug messages to stderr')


    args = parser.parse_args(args)
    return args
