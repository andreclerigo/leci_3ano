all: enc dec

enc: ed.o key.o
	$(CC) -o $@ $^ -lcrypto

dec: ed.o key.o
	$(CC) -o $@ $^ -lcrypto
