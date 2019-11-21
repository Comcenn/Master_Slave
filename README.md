/********************************/
/*           ReadMe             */
/********************************/

---------------|
File Structure |
---------------|

Here is what the directory structure should look like:

	Master_Slave -> REAME.md
	           | -> requirements.txt
		       | -> poetry.lock
			   |
		       -- master -> master.py
			   |         -> __init__.py
			   |
			   -- slave -> slave.py
			   |        -> __init__.py
			   |
			   -- tests -> test_master.py
			            -> test_slave.py
						-> __init__.py

If it does not look like this please reorganise the files so that they adhere
to this tree structure.


------|
Setup |
------|

This program was built using Python 3.7.2(64 bit version) however it should work with
the 32 bit version.

Please download the above version of Python and create a virtual environment.

Once this is done activate the environment and either install the require packages 
using the 'requirements.txt' file and pip:

	pip install -r <path to requirements.txt>

Or if you use Poetry to manage your projects install it and then change into programs
top level directory and enter:

	poetry install

Once these steps are carried out you will be able to run the program.


------------------|
Running the Tests |
------------------|

Please activate your virtual environment you setup in the Setup section above and
change into the programs top level directory once there type:

	python -m unittest discover

This should discover and run all the unittests for the program in the 'tests' 
directory.

Please Note:
	
	You may find the tests all pass but you get:

		"sys:1: RuntimeWarning: coroutine 'async_mock.<locals>.mock_coro' was never awaited"
	
	Please ignore its to do with how I setup the mock co routines and I have not got time to 
	sort it out.


--------------------|
Running the Program |
--------------------|

Again please activate your virtual environment and simply type:

	python <path to the master.py file>

You can also pass in the path to the 'slave.py' file using the
'--slavePath' option:

	python <path to the master.py file> --slavePath <path to the slave.py file>

If you keep the same file structure you should not need to.

