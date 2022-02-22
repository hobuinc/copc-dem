from .bounds import Bounds 
from .copc import COPC
from .logs import logger

import pdal
import uuid

class Tile(object):
    def __init__(self, filename, bounds, last_count=None, args=None) -> None:
        self.bounds = bounds
        if isinstance(filename, COPC):
            filename = filename.filename

        self.copc = COPC(filename, bounds)
        self.last_count = last_count
        self.args = args

    def split(self, threshold):

        count = self.copc.count

        if not self.last_count:
            self.last_count = threshold

        logger.info(f'split() self.copc.count {self.copc.count} self.last_count {self.last_count} count {count} self.bounds {self.bounds}')
        if count == self.last_count: # we bottomed out because the hierarchy does not split anymore
            logger.debug(f'self.count == self.copc.count, splitting has stopped')
            yield self
        if count < threshold:
            logger.debug(f'count {count} < threshold {threshold}')
            self.last_count = count
            yield self
        else:
            logger.info(f'splitting again based on threshold')

            for b in self.bounds.split():
                t = Tile(self.copc.filename, b, count, args=self.args)
                t.last_count = count

                yield t.split(threshold) 

    
    def pipeline(self):

        name = uuid.uuid4()
        filename = f"{self.args.output_dir}/{self.args.output_type}-{name}.tif"
        writer = pdal.Writer.gdal(
            filename,
            bounds=str(self.bounds),
            data_type="float32",
            output_type = self.args.output_type,
            resolution=self.args.write_resolution,
        )
        bounds = self.bounds.buffer(self.args.collar) 
        p = self.copc.reader(bounds, self.args.read_resolution, self.args.collar ) | writer
        return p

    def __str__(self):
        return f'{self.bounds} - {self.copc.filename} - {self.last_count}'



# def split(copc, bounds, resolution, output,  threshold=50000):
#     info = copc.compute_quickinfo(bounds, resolution)
#     count = info['num_points']

#     try:
#         bounds.count
#     except AttributeError:

#         bounds.count = 0
# #     logger.debug(f"bounds.count {bounds.count:,} count: {count:,}")
#     if count == bounds.count: # we bottomed out
# #         logger.debug(f"Split to {info['num_points']} for bounds {bounds}")
#         output.append(bounds)
#         return

#     if count < threshold:
# #         logger.debug(f"Threshold to {info['num_points']} for bounds {bounds}")
#         output.append(bounds)
#         return
#     else:
#         tiles = bounds.split()
#         for t in tiles:
#             t.count = count
#             split(copc, t, resolution, output, threshold)
