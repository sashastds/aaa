##### Issue 1 run command
python -m doctest -v -o NORMALIZE_WHITESPACE issue1.py > issue1.result
##### Issue 2 run command
pytest -v test_issue2.py > issue2.result
##### Issue 3 run command
python issue3.py 2> issue3.result
##### Issue 4 run command
pytest -v test_issue4.py > issue4.result
##### Issue 5 run command
pytest --cov --cov-branch -v test_issue5.py > issue5.result
coverage html

