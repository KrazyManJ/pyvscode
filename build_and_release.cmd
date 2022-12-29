python -m build
set /p token=<token.txt
twine upload dist/* -u __token__ -p %token%