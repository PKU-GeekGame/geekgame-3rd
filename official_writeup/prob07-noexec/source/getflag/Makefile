Q  ?= @

ECHO   := echo -e '\t'
CARGO  := cargo build --release
CD     := cd

.PHONY: all
all: easy_flag hard_flag

.PHONY: easy_flag
easy_flag:
	$(Q)$(ECHO) MAKE easy_flag
	$(Q)$(MAKE) -C easy_flag

.PHONY: hard_flag
hard_flag:
	$(Q)$(ECHO) CARGO hard_flag
	$(Q)$(CD) hard_flag && $(CARGO)
