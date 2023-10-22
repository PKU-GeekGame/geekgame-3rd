SOURCE  := easy_flag.S
TARGET  := easy_flag

Q  ?= @

CC   := gcc
ECHO := echo -e '\t'

CFLAGS  := -nostdlib -static

.PHONY: all
all: $(TARGET)

$(TARGET): $(SOURCE)
	$(Q)$(ECHO) CC $(TARGET)
	$(Q)$(CC) -o $(TARGET) $(CFLAGS) $(SOURCE)
