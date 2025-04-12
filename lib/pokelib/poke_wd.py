class WatchDog():
    def __init__(self, time_out, _callback = None):
        self.next_t = time.time()
        self.i = time_out
        self.done = False
        self.time_out = time_out
        self.callback = _callback
        self._run()

    def _run(self):
        print("WATCHDOG hello {}, done {}".format(self.i,self.done))
        self.next_t-=1
        self.i-=1
        time.sleep(1)
        if self.i < 0:
            print("WATCHDOG callback ")
            self.callback()
        if not self.done:
            # print("WATCHDOG  start thread ")
            threading.Timer( self.next_t - time.time(), self._run).start()
    
    def stop(self):
        self.done=True
    
    def reset(self):
        self.i = self.time_out
        
    def kill(self):
        print("WATCHDOG  end all ")
        os.kill(threading.main_thread().native_id, signal.SIGKILL)
        sys.exit(0)
    
