from urllib import request
import pdal
from pyproj import CRS

from . import logs
from .bounds import Bounds, MaxBounds

import json

class COPC(object):
    def __init__(self, filename, bounds = None):

        self.filename = filename
        self.info =  self.compute_quickinfo(bounds)

        bounds_dict = self.info["bounds"]
        minx, miny, minz = (
            bounds_dict["minx"],
            bounds_dict["miny"],
            bounds_dict["minz"],
        )
        maxx, maxy, maxz = (
            bounds_dict["maxx"],
            bounds_dict["maxy"],
            bounds_dict["maxz"],
        )
        srs = CRS(self.info["srs"]["compoundwkt"])
        self.bounds = Bounds(minx, miny, maxx, maxy, self.info['resolution'], srs)


    def get_count(self):
        return self.info['num_points']
    count = property(get_count)

    def reader(self, bounds = None, resolution = None, buffer = None):
        reader = pdal.Reader.copc(self.filename)

        if bounds:
            b = bounds
            if buffer:
                b = bounds.buffer(buffer)
            reader._options["bounds"] = str(b)
        if resolution:
            reader._options["resolution"] = resolution
        requests = 3
        if requests:
            reader._options["requests"] = requests
        return reader

    def compute_quickinfo(self, bounds, buffer = None):
        if not bounds:
            resolution = 20000
        else:
            resolution = bounds.resolution

        requests = 3
        reader = self.reader(bounds, resolution, buffer)
        p = reader.pipeline()

        if logs.logger.level < logs.logging.INFO:
            p.loglevel = logs.logger.level
        info = p.quickinfo["readers.copc"]

        info['resolution'] = resolution
        if logs.logger.level < logs.logging.INFO:
            output = p.log.strip()
            if output:
                logs.logger.debug(f"PDAL: {p.log.strip()}")
        return info



