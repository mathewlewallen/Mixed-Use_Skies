.PHONY: all closure blockdiag reliability containment

all: closure blockdiag reliability containment

closure:
	cd closure_example && python make_closure_example.py hazard.csv closure_example.png || echo "Provide closure_example/hazard.csv first."

blockdiag:
	cd blockdiag && (dot -Tpng blockdiag.dot -o blockdiag.png || python make_blockdiag.py)

reliability:
	cd reliability_plot && python make_reliability_plot.py preds.csv reliability_plot.png --bins 4 || echo "Provide reliability_plot/preds.csv first."

containment:
	cd containment_demo && python make_containment_demo.py --eps 0.20 --outfile containment_demo.png
