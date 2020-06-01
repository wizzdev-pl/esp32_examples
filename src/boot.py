import gc

import uos
import logging

main_logger = logging.getLogger(None)
main_logger.setLevel(logging.DEBUG)
logging.debug("In BOOT.")


# Diagnostic info - not needed in production
gc.collect()
logging.debug('free memory: ' + str(gc.mem_free()))

fs_stat = uos.statvfs('//')
logging.info('Free flash: {0} MB'.format((fs_stat[0]*fs_stat[3])/1048576))
