MVE_ROOT := ../..
TARGET := ${MVE_ROOT}/mve_libs/libmve_fssr.a
include ${MVE_ROOT}/Makefile.inc

CXXFLAGS += -fPIC -I${MVE_ROOT}/libs ${OPENMP}
LDLIBS += -lpng -ltiff -ljpeg ${OPENMP}

SOURCES := $(wildcard [^_]*.cc)
${TARGET}: ${SOURCES:.cc=.o}
	$(AR) rcs $@ $^

clean:
	${RM} $(TARGET) *.o Makefile.dep

.PHONY: clean
