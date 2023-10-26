LLVM_DIR    := llvm-project
LLVM_SRC    := $(LLVM_DIR)/llvm
LLVM_REPO   := https://github.com/llvm/llvm-project.git
LLVM_BUILD  := llvm-build
LLVM_TAG    := llvmorg-17.0.1
PATCH_FILE  := noexec.patch

LLVM_TARGETS  := lldb lldb-server

Q  ?= @

ECHO      := echo -e '\t'
MKDIR     := mkdir
GITCLONE  := git clone --depth=1
PATCH     := patch -p1
CMAKE     := cmake
NINJA     := ninja

CMAKEFLAGS  := -G Ninja \
	       -DLLVM_ENABLE_PROJECTS="clang;lldb" \
	       -DCMAKE_EXE_LINKER_FLAGS=-static \
	       -DCMAKE_BUILD_TYPE=Release \
	       -DLLDB_ENABLE_LIBEDIT=Off \
	       -DLLDB_ENABLE_CURSES=Off \
	       -DLLDB_ENABLE_LZMA=Off \
	       -DLLDB_ENABLE_LIBXML2=Off \
	       -DLLDB_ENABLE_PYTHON=Off \
	       -DLLDB_ENABLE_LUA=Off \
	       -DLLVM_ENABLE_ZLIB=Off \
	       -DLLVM_ENABLE_ZSTD=Off

.PHONY: all
all: $(LLVM_DIR) $(LLVM_BUILD)
	$(Q)$(ECHO) CMAKE $(LLVM_DIR)
	$(Q)$(CMAKE) $(CMAKEFLAGS) -S $(LLVM_SRC) -B $(LLVM_BUILD)
	$(Q)$(ECHO) NINJA $(LLVM_BUILD)
	$(Q)$(NINJA) -C $(LLVM_BUILD) $(LLVM_TARGETS)

$(LLVM_DIR):
	$(Q)$(ECHO) GITCLONE $(LLVM_REPO)
	$(Q)$(GITCLONE) --branch=$(LLVM_TAG) $(LLVM_REPO) $(LLVM_DIR)
	$(Q)$(ECHO) PATCH $(PATCH_FILE)
	$(Q)$(PATCH) -d $(LLVM_DIR) < $(PATCH_FILE)

$(LLVM_BUILD):
	$(Q)$(ECHO) MKDIR $(LLVM_BUILD)
	$(Q)$(MKDIR) $(LLVM_BUILD)
