# -*- coding: utf-8 -*-
## @package proxen.proxen
# @brief Main application entry-point module that creates and launches the GUI app -- see main() function.
import os, sys, traceback
from qtimports import QtCore, QtWidgets

# ======================================================================================= #
URL = 'https://open.spotify.com/track/4BrYTZfpZzeNAGbJ7kh2Z0?si=2250d6630b424bb7'

## Main function that creates and launches the application.
def main():

    from gui import MainWindow
    
    try:        
        # change working dir to current
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # initialize Qt Core App settings
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        # disable Qt debug messages
        QtCore.qInstallMessageHandler(lambda msg_type, msg_log_context, msg_string: None)
        # create QApplication instance
        app = QtWidgets.QApplication(sys.argv)
        # create main window
        mw = MainWindow(QtCore.QUrl.fromUserInput(sys.argv[1]) if len(sys.argv) > 1 else QtCore.QUrl(URL))
        # show window
        mw.resize(1800, 968)
        mw.show()
        # run app's event loop
        sys.exit(app.exec())

    except SystemExit as err:
        if str(err) != '0':
            traceback.print_exc(limit=None)

    except Exception as err:
        traceback.print_exc(limit=None)
        sys.exit(1)

    except:
        traceback.print_exc(limit=None)
        sys.exit(1)

# ======================================================================================= #    

## Program entry point.
if __name__ == '__main__':
    main()
