---
title: MI200 GPUFS smoke-kernel checkpoint
tags:
    - x86
    - amdgpu
    - gfx90a
layout: default
permalink: resources/x86-mi200-gpu-fs-smoke-checkpoint
shortdoc: >
    Configuration for creating the MI200 GPUFS smoke-kernel checkpoint.
---

# Resource: `x86-mi200-gpu-fs-smoke-checkpoint`

This directory contains the gem5 configuration and HIP loader used to create
the MI200 full-system CI checkpoint. Linux and the ROCm 7.0 AMDGPU/KFD driver
are initialized first. The loader then initializes HIP, allocates host-visible
memory, loads the `x86-mi200-gpu-fs-smoke` `gfx90a` code object, completes one
warm-up dispatch, resets the test value, and takes the final checkpoint. The
restored system launches and verifies the kernel again.

The final resource is specialized for this smoke kernel. Its saved state
already contains the loaded module, resolved `_Z9incrementPi` function,
kernel argument, and completed warm-up dispatch. It cannot accept another
kernel after restoration. The intermediate loader-stage checkpoint described
below can load another compatible `gfx90a` code object, but it does not provide
the final checkpoint's fast restore path.

The configuration uses an Atomic x86 CPU, so KVM is not required. It obtains
version `1.0.0` of both `x86-ubuntu-24.04-gpu-img` and
`x86-linux-kernel-6.8.0-gpu`.

Build the VEGA_X86 simulator in a gem5 checkout containing the corresponding
MI200 checkpoint support. Create the initialized loader checkpoint first:

```sh
gem5/build/VEGA_X86/gem5.opt \
    gem5-resources/src/x86-mi200-gpu-fs-smoke-checkpoint/\
create-checkpoint.py \
    --gem5-root=gem5 \
    --stage=loader \
    --checkpoint-dir=m5out/mi200-hip-loader
```

Then restore the loader, supply the smoke code object, complete the one-time
module and dispatch warmup, and take the final checkpoint:

```sh
gem5/build/VEGA_X86/gem5.opt \
    gem5-resources/src/x86-mi200-gpu-fs-smoke-checkpoint/\
create-checkpoint.py \
    --gem5-root=gem5 \
    --stage=kernel \
    --loader-checkpoint=m5out/mi200-hip-loader \
    --kernel-binary=gem5-resources/src/x86-mi200-gpu-fs-smoke/\
x86-mi200-gpu-fs-smoke \
    --checkpoint-dir=m5out/x86-mi200-gpu-fs-smoke-checkpoint
```

The loader-stage checkpoint remains useful locally: restoring it with a
different `gfx90a` code object loads that object after restoration. The final
distributed checkpoint is intentionally tied to the smoke kernel so pull
request CI pays only the kernel launch and synchronization cost.

Create the upload archive with the checkpoint files at the archive root:

```sh
COPYFILE_DISABLE=1 tar -C m5out/x86-mi200-gpu-fs-smoke-checkpoint -cf \
    x86-mi200-gpu-fs-smoke-checkpoint.tar .
```

`COPYFILE_DISABLE=1` prevents macOS `tar` from adding `._*` AppleDouble files.
Those extra files would change gem5's extracted-directory checksum.
