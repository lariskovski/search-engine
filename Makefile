.PHONY:  indexer crawler searcher ranker graph

all:
	@echo "hello"

index: 
	@python indexer/indexer.py

cindex: 
	@python indexer/consumer.py

cgraph:
	@python graph/consumer.py

ranker:
	@python ranker/ranker.py
	@python ranker/api.py

searcher:
	@python searcher/searcher_api.py

crawler: 
	@python crawler/crawler.py

 
