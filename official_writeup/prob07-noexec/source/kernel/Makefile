KERNEL_TAR   := linux-6.1.55.tar.xz
KERNEL_DIR   := linux-6.1.55
KERNEL_URL   := https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.55.tar.xz
CONFIG_FILE  := noexec-config
PATCH_FILE   := noexec.patch
CONFIG_DEST  := .config

Q  ?= @

ECHO   := echo -e '\t'
CURL   := curl
UNTAR  := tar xf
PATCH  := patch -p1
RM     := rm -f
CP     := cp

.PHONY: all
all: $(KERNEL_DIR)
	$(Q)$(ECHO) MAKE $(KERNEL_DIR)
	$(Q)$(MAKE) -C $(KERNEL_DIR)

$(KERNEL_DIR): $(KERNEL_TAR) $(CONFIG_FILE) $(PATCH_FILE)
	$(Q)$(ECHO) RM $(KERNEL_DIR)
	$(Q)$(RM) -r $(KERNEL_DIR)
	$(Q)$(ECHO) UNTAR $(KERNEL_TAR)
	$(Q)$(UNTAR) $(KERNEL_TAR)
	$(Q)$(ECHO) CP $(CONFIG_FILE)
	$(Q)$(CP) $(CONFIG_FILE) $(KERNEL_DIR)/$(CONFIG_DEST)
	$(Q)$(ECHO) PATCH $(PATCH_FILE)
	$(Q)$(PATCH) -d $(KERNEL_DIR) < $(PATCH_FILE)

$(KERNEL_TAR):
	$(Q)$(ECHO) CURL $(KERNEL_URL)
	$(Q)$(CURL) $(KERNEL_URL) -o $(KERNEL_TAR)
