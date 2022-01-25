CXXFLAGS = -Wall -ggdb -pthread

LDFLAGS = -pthread -lm

TARGETS = client-server

all:		$(TARGETS)

client-server:    	client-server.o  thread.o utils.o
			g++ -o $@ $^ $(LDFLAGS)

fifo_unsafe.o fifo_bwsafe.o fifo_safe.o:	fifo.h

thread.o utils.o:	%.o:	%.h dbc.h

clean:
			rm -f *.o *~

cleanall:		clean
			rm -f $(TARGETS)
