from asyncio.log import logger
from . import copc
from . import tile
from . import bounds
from .logs import logger 

def doIt(args):
    logger.info(f"opening {args.copc_file} for processing")
    c = copc.COPC(args.copc_file)


    # 294477,5037224 : 302205,5043954
    # minx = 294477
    # maxx = 302205
    # miny = 5037224
    # maxy = 5043954
    # READ_RESOLUTION = 0
    # WRITE_RESOLUTION = 1
    # THRESHOLD = 2000000
    # b = bounds.Bounds(minx, miny, maxx, maxy, READ_RESOLUTION)
    # c = copc.COPC('montreal/montreal-2015.copc.laz', b)
    # c = copc.COPC('montreal/montreal-2015.copc.laz')
    c.bounds.resolution = args.read_resolution

    t = tile.Tile(c.filename, c.bounds, args=args)

    import dask
    from dask.distributed import Client, LocalCluster
    from dask.distributed import wait, progress
    import types
    g = t.split(args.threshold)

    global count
    count = 0

    client = Client()


    batchsize = 20
    global batch 
    batch = []
    global batches 
    batches = []

    def doBatch(seq):
        for x in seq:
            x.execute()


    def process(pipeline):
        pipeline.execute()

    def unpack(g):
        global count
        global batches
        global batch

        while True:
            try:
                k = next(g)
                if isinstance(k, types.GeneratorType):
                    unpack(k)
                elif isinstance(k, tile.Tile):
                    count = count + 1
                    p = k.pipeline()

                    # d = dask.delayed(process)(p)
                    batch.append(p)
                    if len(batch) == batchsize:
                        d = dask.delayed(doBatch)(batch)
                        batches.append(d)
                        batch = []
                    break

            except StopIteration:
                # leaf
                break


    unpack(g)


    if len(batch):
        d = dask.delayed(doBatch)(batch)
        batches.append(d)

    data = dask.compute(*batches)

    wait(data)
