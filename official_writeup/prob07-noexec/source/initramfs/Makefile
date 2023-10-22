OUT  := ../deploy
ROOT := root

COMMON_DIRS  := bin
COMMON_FILES := bin/busybox init
LLDB_BINS    := ../llvm/llvm-build/bin/lldb-server ../llvm/llvm-build/bin/lldb
LLDB_ROOT    := bin
GETFLAG_BIN  := ../getflag/hard_flag/target/release/hard_flag
GETFLAG_LIBS := $(shell ldd $(GETFLAG_BIN) | grep '=>' | cut -f3 -d' ')
GETFLAG_RTS  := usr usr/lib
GETFLAG_ROOT := usr/lib

EASY_IMG     := $(OUT)/easy.cpio.gz
EASY_DIRS    := $(COMMON_DIRS)
EASY_FILES   := $(COMMON_FILES) \
		$(addprefix $(LLDB_ROOT)/, $(notdir $(LLDB_BINS)))

HARD_IMG     := $(OUT)/hard.cpio.gz
HARD_DIRS    := $(COMMON_DIRS) $(GETFLAG_RTS)
HARD_FILES   := $(COMMON_FILES) \
		$(addprefix $(GETFLAG_ROOT)/, $(notdir $(GETFLAG_BIN) $(GETFLAG_LIBS)))

Q  ?= @

MKDIR   := mkdir -p
CPIO    := cpio
ECHO    := echo -e '\t'
PRINTLN := printf '%s\n'
GZIP    := gzip -9 -n
CP      := cp
STRIP   := strip -s

CPIO_FLAGS    := -R 0:0 --quiet -H newc

.PHONY: all
all: $(OUT) $(EASY_IMG) $(HARD_IMG)

$(OUT) $(ROOT)/$(GETFLAG_ROOT):
	$(Q)$(ECHO) MKDIR $@
	$(Q)$(MKDIR) $@

define BINARY_COPY =
$$(ROOT)/$(2)/$$(notdir $(1)): $(1) | $(ROOT)/$(2)
	$$(Q)$$(ECHO) CP $(1)
	$$(Q)$$(CP) $$< $$@
	$$(Q)$$(ECHO) STRIP $(1)
	$$(Q)$$(STRIP) $$@
endef

$(foreach target, $(GETFLAG_BIN) $(GETFLAG_LIBS), \
	$(eval $(call BINARY_COPY,$(target),$(GETFLAG_ROOT))))

$(foreach target, $(LLDB_BINS), \
	$(eval $(call BINARY_COPY,$(target),$(LLDB_ROOT))))

$(EASY_IMG): $(addprefix $(ROOT)/, $(EASY_FILES))
	$(Q)$(ECHO) CPIO $(EASY_IMG)
	$(Q)$(PRINTLN) $(EASY_DIRS) $(EASY_FILES) | \
		$(CPIO) -o -D $(ROOT) $(CPIO_FLAGS) | \
		$(GZIP) > $(EASY_IMG)

$(HARD_IMG): $(addprefix $(ROOT)/, $(HARD_FILES)) \
			| $(ROOT)/$(GETFLAG_ROOT)
	$(Q)$(ECHO) CPIO $(HARD_IMG)
	$(Q)$(PRINTLN) $(HARD_DIRS) $(HARD_FILES) | \
		$(CPIO) -o -D $(ROOT) $(CPIO_FLAGS) | \
		$(GZIP) > $(HARD_IMG)
