Steps to run the code:-
Step1: Download flask_lcs.py

Step2: Open a terminal.

Step3: Type this in the terminal:-
	export FLASK_APP=<Path to flask_lcs.py>

Step4: On a serperate terminal execute curl request:-
	curl localhost:5000/lcs -d '{"setOfStrings" : [{"value":"commute"},{"value":"communicate"},{"value":"commutation"}]}' -H 'Content-Type: application/json'