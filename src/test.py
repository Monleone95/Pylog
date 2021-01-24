from pylog import Logger, Loggable, TEE

class Main(Loggable):
    def __init__(self):
        super().__init__()
        self.logger.setOutput(TEE)

    def run(self):
        self.debug('hi world')
        self.info('my name is logger')
        self.notice('see how i log you')

class SubClass(Loggable):
    def __init__(self):
        super().__init__()
        self.logger.setOutput(TEE)

    def run(self):
        self.debug('hi world')
        self.info('my name is logger')
        self.notice('see how i log you')

if __name__ == '__main__':
    log = Logger()
    log.setOutput(TEE)
    log.critical('Hey im the script')
    Main().run()
    SubClass().run()
