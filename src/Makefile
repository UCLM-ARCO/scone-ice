all:

clean:
	$(RM) *~ proxy.out

run-server:
	./Server.py --Ice.Config=Server.config

run-client:
	./Client.py "$(shell head -1 proxy.out)"
