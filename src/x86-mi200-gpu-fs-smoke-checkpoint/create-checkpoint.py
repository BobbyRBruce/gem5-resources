# Copyright (c) 2026 The Regents of The University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer; redistributions in
# binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution; neither the name of the copyright
# holders nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Create the MI200 GPUFS smoke-kernel checkpoint resource."""

import argparse
import sys
from pathlib import Path

from m5.util import addToPath

parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
parser.add_argument(
    "--gem5-root",
    type=Path,
    required=True,
    help="Path to a gem5 checkout containing the MI200 GPUFS config",
)
parser.add_argument(
    "--resource-directory",
    type=Path,
    default=Path(__file__).resolve().parent / "resources",
)
parser.add_argument("--stage", choices=("loader", "kernel"), required=True)
parser.add_argument(
    "--loader-checkpoint",
    type=Path,
    help="Initialized loader checkpoint produced by the loader stage",
)
parser.add_argument(
    "--kernel-binary",
    type=Path,
    help="gfx90a code object to load before the final checkpoint",
)
args, remaining_args = parser.parse_known_args()
if not any(
    arg == "--checkpoint-dir" or arg.startswith("--checkpoint-dir=")
    for arg in remaining_args
):
    parser.error("--checkpoint-dir is required")
sys.argv[1:] = remaining_args

gem5_root = args.gem5_root.resolve()
addToPath(str(gem5_root / "configs"))
addToPath(str(gem5_root / "configs" / "example" / "gpufs"))

from mi200 import runMI200GPUFS

from gem5.resources.resource import (
    CheckpointResource,
    FileResource,
    obtain_resource,
)

resource_kwargs = {
    "resource_directory": str(args.resource_directory),
    "resource_version": "1.0.0",
}

source_directory = Path(__file__).resolve().parent
if args.stage == "loader":
    if args.loader_checkpoint or args.kernel_binary:
        parser.error(
            "--loader-checkpoint and --kernel-binary are only valid for the "
            "kernel stage"
        )
    checkpoint = None
    application = FileResource(
        local_path=str(source_directory / "hip-checkpoint-runner.py")
    )
    application_is_kernel_object = False
    extra_boot_options = ("init=/home/gem5/run_gem5_app.sh",)
else:
    if not args.loader_checkpoint or not args.kernel_binary:
        parser.error(
            "the kernel stage requires --loader-checkpoint and --kernel-binary"
        )
    checkpoint = CheckpointResource(local_path=str(args.loader_checkpoint))
    application = FileResource(local_path=str(args.kernel_binary))
    application_is_kernel_object = True
    extra_boot_options = ()

runMI200GPUFS(
    cpu_type="X86AtomicSimpleCPU",
    disk=obtain_resource("x86-ubuntu-24.04-gpu-img", **resource_kwargs),
    kernel=obtain_resource("x86-linux-kernel-6.8.0-gpu", **resource_kwargs),
    app=application,
    checkpoint=checkpoint,
    system_memory="2GiB",
    extra_boot_options=extra_boot_options,
    application_is_kernel_object=application_is_kernel_object,
)
