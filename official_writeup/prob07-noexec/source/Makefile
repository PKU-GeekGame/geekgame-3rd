CHALLENGE_TAR   := noexec-challenge.tar.xz
GIVEUSER_TAR    := noexec-give_to_user.tar.xz

KERNELIMG_SRC   := kernel/linux-6.1.55/arch/x86_64/boot/bzImage

RUN_ENTRY       := deploy/run.sh
KERNELIMG_DST   := deploy/bzImage
EASY_CPIO       := deploy/easy.cpio.gz
HARD_CPIO       := deploy/hard.cpio.gz
GIVEUSER_FILES  := $(RUN_ENTRY) \
		   $(KERNELIMG_DST) \
		   $(EASY_CPIO) \
		   $(HARD_CPIO) \
		   deploy/flag1.txt \
		   deploy/flag2.txt \
		   deploy/flag3.txt

Q  ?= @

ECHO  := echo -e '\t'
TAR   := tar c
CP    := cp
XZ    := xz

.PHONY: all
all: $(GIVEUSER_FILES)

define SUBTARGET
.PHONY: $(1)
$(1): $(2)
	$$(Q)$$(ECHO) MAKE $(1)
	$$(Q)$$(MAKE) -C $(1)
endef

$(eval $(call SUBTARGET,kernel,))
$(eval $(call SUBTARGET,llvm,))
$(eval $(call SUBTARGET,getflag,))
$(eval $(call SUBTARGET,initramfs,llvm getflag))

.PHONY: run
run: all
	$(Q)$(ECHO) RUN
	$(Q)$(RUN_ENTRY)

.PHONY: package
package: $(GIVEUSER_TAR)

$(GIVEUSER_TAR): $(GIVEUSER_FILES)
	$(Q)$(ECHO) PACKAGE $(GIVEUSER_TAR)
	$(Q)$(TAR) $(GIVEUSER_FILES) | $(XZ) > $(GIVEUSER_TAR)

$(KERNELIMG_DST): $(KERNELIMG_SRC)
	$(Q)$(ECHO) CP $(KERNELIMG_DST)
	$(Q)$(CP) $(KERNELIMG_SRC) $(KERNELIMG_DST)

$(KERNELIMG_SRC): kernel

$(EASY_CPIO) $(HARD_CPIO): initramfs
