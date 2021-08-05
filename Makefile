.PHONY:  index crawler search rank graph

all:
	@echo "hello"

index: 
	@python index/indexer_api.py

cindex: 
	@python index/consumer.py

cgraph:
	@python graph/consumer.py

ranker:
	@python rank/ranker.py
	@python rank/ranker_api.py

searcher:
	@python search/searcher_api.py

crawler: 
	@python crawler/crawler.py

 
