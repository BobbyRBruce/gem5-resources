HIPCC ?= /opt/rocm/bin/hipcc
TARGET := x86-mi200-gpu-fs-smoke

.PHONY: all clean

all: $(TARGET)

$(TARGET): gpu_checkpoint_smoke.cpp
	$(HIPCC) -O2 --genco --offload-arch=gfx90a $< -o $@

clean:
	rm -f $(TARGET)
