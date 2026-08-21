---
title: MI200 GPUFS checkpoint smoke kernel
tags:
    - x86
    - amdgpu
    - gfx90a
layout: default
permalink: resources/x86-mi200-gpu-fs-smoke
shortdoc: >
    Source for the MI200 GPUFS checkpoint smoke code object.
---

# Resource: `x86-mi200-gpu-fs-smoke`

This directory builds the HIP code object used to validate the
`x86-mi200-gpu-fs-smoke-checkpoint` resource. Its `gfx90a` kernel increments
one host-visible integer. The checkpoint's initialized HIP loader launches
the kernel, synchronizes, and checks the result.

Build it with a ROCm installation containing `hipcc`:

```sh
make
```

Set `HIPCC` if ROCm is installed somewhere other than `/opt/rocm`:

```sh
make HIPCC=/path/to/hipcc
```

The output is `x86-mi200-gpu-fs-smoke` in this directory.
