import time
import argparse
import logging
import os
import schedule

from kubeenforce import KubeEnforce

logger = logging.getLogger('main')

if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s %(name)s] %(message)s',level=3)
    logging.info('Started')
    newEnforcer = KubeEnforce()
    newEnforcer.run()
    schedule.every(10).minutes.do(newEnforcer.run)
    logging.info('Finished')
    while True:
        schedule.run_pending()
        time.sleep(1)