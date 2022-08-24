from qtimports import QtCore, Signal, Slot
import traceback

# ******************************************************************************** #
# *****          QThreadStump
# ******************************************************************************** #

## Customized thread class (based on QThread) that adds
# progress, error etc. signals and mutex locking to avoid thread racing.
class QThreadStump(QtCore.QThread):

    ## Error signal (args are: instance of this thread and the error message)
    sig_error = Signal(QtCore.QThread, str)

    ## @param priority `int` thread default priority (default = normal)
    # @param on_start `callable` callback function called before the main
    # operation is executed (callback has no args or returned result)
    # @param on_finish `callable` callback function called after the main
    # operation completes (callback has no args or returned result)
    # @param on_run `callable` callback function for the main
    # operation (callback has no args or returned result)
    # @param on_error `callable` callback function to handle exceptions
    # raised during the thread operation (see QThreadStump::sig_error)
    # @param start_signal `Signal` signal that can be connected to
    # the `start` slot (if not `None`)
    # @param stop_signal `Signal` signal that can be connected to
    # the `terminate` slot (if not `None`)
    # @param free_on_finish `bool` whether the thread instance will be deleted
    # from memory after it completes its operation (default = `False`)    
    # @param can_terminate `bool` whether the thread can be terminated (default = `True`)
    # @param start_now `bool` whether to start the thread upon creation (default = `False`)
    def __init__(self, priority=QtCore.QThread.NormalPriority,
                 on_start=None, on_finish=None, on_run=None, on_error=None,
                 start_signal=None, stop_signal=None,
                 free_on_finish=False, can_terminate=True, start_now=False):
        super().__init__()
        ## `int` thread default priority (default = normal)
        self.priority = priority
        ## `callable` callback function executed before the thread runs
        self.on_start = on_start
        ## `callable` callback function executed after the thread finishes
        self.on_finish = on_finish
        ## `callable` callback function for the main operation
        self.on_run = on_run
        ## `callable` callback function executed when an exception occurs
        self.on_error = on_error
        ## `bool` whether the thread instance will be deleted from memory after it completes
        self.free_on_finish = free_on_finish
        ## `bool` whether the thread can be terminated
        self.can_terminate = can_terminate
        ## `Signal` signal that can be connected to the `start` slot (if not `None`)
        self.start_signal = start_signal
        ## `Signal` signal that can be connected to the `terminate` slot (if not `None`)
        self.stop_signal = stop_signal
        ## `QtCore.QMutex` mutex lock used by QThreadStump::lock() and QThreadStump::unlock()
        self.mutex = QtCore.QMutex()
        if start_now: self.start()

    ## Destructor: waits for the thread to complete.
    def __del__(self):
        try:
            self.wait()
        except:
            pass

    ## `int` getter for `QtCore.QThread.default_priority` (thread priority)
    @property
    def priority(self):
        return self.default_priority

    ## sets `QtCore.QThread.default_priority` (thread priority)
    @priority.setter
    def priority(self, _priority):
        try:
            self.default_priority = _priority if _priority != QtCore.QThread.InheritPriority else QtCore.QThread.NormalPriority
        except:
            pass

    ## `callable` getter for QThreadStump::_on_start
    @property
    def on_start(self):
        return self._on_start

    ## setter for QThreadStump::_on_start
    @on_start.setter
    def on_start(self, _on_start):
        try:
            self.started.disconnect()
        except:
            pass
        ## `callable` callback function executed before the thread runs
        self._on_start = _on_start
        if self._on_start:
            self.started.connect(self._on_start)

    ## `callable` getter for QThreadStump::_on_finish
    @property
    def on_finish(self):
        return self._on_finish

    ## setter for QThreadStump::_on_finish
    @on_finish.setter
    def on_finish(self, _on_finish):
        try:
            self.finished.disconnect()
        except:
            pass
        ## `callable` callback function executed after the thread finishes
        self._on_finish = _on_finish
        if self._on_finish:
            self.finished.connect(self._on_finish)
        if getattr(self, '_free_on_finish', False):
            self.finished.connect(self.deleteLater)

    ## `bool` getter for QThreadStump::_free_on_finish
    @property
    def free_on_finish(self):
        return self._free_on_finish

    ## setter for QThreadStump::_free_on_finish
    @free_on_finish.setter
    def free_on_finish(self, _free_on_finish):
        try:
            self.finished.disconnect()
        except:
            pass
        ## `bool` whether the thread instance will be deleted from memory after it completes
        self._free_on_finish = _free_on_finish
        if getattr(self, '_on_finish', None):
            self.finished.connect(self._on_finish)
        if self._free_on_finish:
            self.finished.connect(self.deleteLater)

    ## `callable` getter for QThreadStump::_on_error
    @property
    def on_error(self):
        return self._on_error

    ## setter for QThreadStump::_on_error
    @on_error.setter
    def on_error(self, _on_error):
        try:
            self.sig_error.disconnect()
        except:
            pass
        ## `callable` callback function executed when an exception occurs
        self._on_error = _on_error
        if self._on_error:
            self.sig_error.connect(self._on_error)

    ## `bool` getter for QThreadStump::_can_terminate
    @property
    def can_terminate(self):
        return self._can_terminate

    ## setter for QThreadStump::_can_terminate
    @can_terminate.setter
    def can_terminate(self, _can_terminate):
        self.setTerminationEnabled(_can_terminate)
        ## `bool` whether the thread can be terminated
        self._can_terminate = _can_terminate

    ## `Signal` getter for QThreadStump::_start_signal
    @property
    def start_signal(self):
        return self._start_signal

    ## setter for QThreadStump::_start_signal
    @start_signal.setter
    def start_signal(self, _start_signal):
        ## `Signal` signal that can be connected to the `start` slot
        self._start_signal = _start_signal
        if self._start_signal:
            self._start_signal.connect(self.start)

    ## `Signal` getter for QThreadStump::_stop_signal
    @property
    def stop_signal(self):
        return self._stop_signal

    ## setter for QThreadStump::_stop_signal
    @stop_signal.setter
    def stop_signal(self, _stop_signal):
        ## `Signal` signal that can be connected to the `terminate` slot
        self._stop_signal = _stop_signal
        if self._stop_signal:
            self._stop_signal.connect(self.terminate)

    ## Locks the internal mutex to preclude data racing.
    def lock(self):
        self.mutex.lock()

    ## Releases the mutex lock.
    def unlock(self):
        self.mutex.unlock()

    ## Executes the worker function pointed to by QThreadStump::on_run.
    def run(self):
        try:
            self.setPriority(self.priority)
        except:
            pass
        if self.on_run and not self.isInterruptionRequested():
            try:
                self.on_run()
            except Exception as err:
                traceback.print_exc(limit=None)
                self.sig_error.emit(self, str(err))