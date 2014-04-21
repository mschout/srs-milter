SBINDIR =	/usr/sbin
MANDIR =	/usr/man/man8
DEFINES =	
INCDIRS =	-I/usr/local/include
LIBDIRS =	-L/usr/local/lib
CFLAGS =	-Wall $(DEFINES) $(INCDIRS)
LDFLAGS =	-g3 $(LIBDIRS)
INSTALL =	/usr/bin/install

all:			srs-milter

srs-milter:		srs-milter.o
	$(CC) $(LDFLAGS) srs-milter.o -lmilter -lpthread -lspf2 -lsrs2 -o srs-milter

.c.o:
	$(CC) $(CFLAGS) -c $<

srs-milter.o:	srs-milter.c


install:		all
	@mkdir -p ${DESTDIR}${SBINDIR}
	${INSTALL} -m 0755 -c srs-milter ${DESTDIR}${SBINDIR}/

clean:
	rm -f srs-milter *.o a.out core
