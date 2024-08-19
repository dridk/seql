

check:
	textx check seql/grammar.tx

view:
	textx generate seql/grammar.tx --overwrite --target dot 
	dot -Tpng -O seql/grammar.dot 
	display seql/grammar.dot.png
view2:
	textx generate test.txt --grammar seql/grammar.tx --overwrite --target dot 
	dot -Tpng -O test.dot 
	display test.dot.png

test:
	python -m pytest --no-header -vv
