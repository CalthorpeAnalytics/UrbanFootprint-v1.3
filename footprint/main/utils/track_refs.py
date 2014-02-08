import logging
import sys

__author__ = 'calthorpe'
logger = logging.getLogger(__name__)

class TrackRefs:
    """Object to track reference counts across test runs."""

    def __init__(self, limit=40):
        self.type2count = {}
        self.type2all = {}
        self.limit = limit

    def update(self):
        obs = sys.getobjects(0)
        type2count = {}
        type2all = {}
        for o in obs:
            all = sys.getrefcount(o)

            if type(o) is str and o == '<dummy key>':
                # avoid dictionary madness
                continue
            t = type(o)
            if t in type2count:
                type2count[t] += 1
                type2all[t] += all
            else:
                type2count[t] = 1
                type2all[t] = all

        ct = [(type2count[t] - self.type2count.get(t, 0),
               type2all[t] - self.type2all.get(t, 0),
               t)
              for t in type2count.iterkeys()]
        ct.sort()
        ct.reverse()
        printed = False

        logger.debug("----------------------")
        logger.debug("Memory profiling")
        i = 0
        for delta1, delta2, t in ct:
            if delta1 or delta2:
                if not printed:
                    logger.debug("%-55s %8s %8s" % ('', 'insts', 'refs'))
                    printed = True

                logger.debug("%-55s %8d %8d" % (t, delta1, delta2))

                i += 1
                if i >= self.limit:
                    break

        self.type2count = type2count
        self.type2all = type2all