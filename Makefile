.PHONY: consumers indexer searchengine crawler

all:
	@echo "hello"

index: 
	@python indexer/indexer.py

cindex: 
	@python indexer/consumer.py

cgraph:
	@python graph/consumer.py

crawler: 
	@python crawler/crawler.py

 
