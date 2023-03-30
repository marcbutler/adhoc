#!/usr/bin/bash

# Run on the an evergreen spawn host through ssh to set
# it up for WiredTiger debugging. See bash/zsh functions below
# as to how to formulate the ssh command line.
#
# Requires bash regular expression support on the host. The 
# version of bash shipped with most modern distributions should
# support this, but older RedHat distros may not.
#
# TODO Add a force option to unpack tar balls irrespective of the
#   state of the artifact directory.
#
# Both the following bash and zsh functions take the full string
# that evergreen web ui copies to the clipboard including 'ssh'.
#
# bash
# +
# function hatch {
#     eval $* "$(< $HOME/path/to/hatch.bash)"
# }
# -
#
# zsh
# +
# function hatch {
#   cmd='$* "$(< $HOME/src/adhoc/hatch.bash)"'
#   eval ${cmd}
# }
# -

function bail_out {
    echo $*; exit 1
}

mci_dir=/data/mci
[[ -d $mci_dir ]] || bail_out "No ${mci_dir} dir found!"

artifacts_dir=$(find $mci_dir -maxdepth 1 -type d -name 'artifacts*')
[[ -z "$artifacts_dir" ]] && bail_out "No artifacts directory in ${mci_dir}!"

src_dir=$(find $mci_dir -maxdepth 1 -type d -name 'source*')
[[ -z "$src_dir" ]] && bail_out "No source directory in ${mci_dir}!"


# Unpack the artifact tarballs on the build host.
#
# TODO To support builds prior to 6.0 switch over to cmake: will need to
# alternately look for a directory 'posix_build'.
#
if [[ -d "$artifacts_dir/cmake_build" ]]; then
    echo "Looks like the artifact tarballs may have already been unpacked."
else
    # TODO Work out the right way to handle artifact tarballs with
    # the same name except for a digit suffix before '.tgz'.

    for tarball in $(find $artifacts_dir -maxdepth 1 -type f -name '*.tgz'); do
        # Use nohup so if the connection is lost the unpacked contents will be 
        # ready next connection attempt.
        nohup tar xf $tarball -C $artifacts_dir &
        echo "Unpacking $tarball ..."
    done
    wait $(jobs -p)

    # TODO See if tcmalloc.*.tgz exists and needs to be unpacked.
fi


# Create a gdbinit configuration for WT core spelunking.
#
gdbinit=$HOME/.gdbinit
if [[ -f $gdbinit ]]; then
    echo "${gdbinit} already present - remove to regenerate."
elif [[ -f $artifacts_dir/cmake_build/test/format/t ]]; then

    # Find a DW_AT_name entry with a recognizable source code path
    # from the WiredTiger source.
    #
    # The test/format binary 't' is crucial so just assume it is
    # there. However release builds appear to strip the test
    # executables.
    #
    # TODO Handle failure gracefully if it is stripped (aka release)
    # binary.
    #
    t_exe=$artifacts_dir/cmake_build/test/format/t
    line=$(objdump -g $t_exe 2>/dev/null | grep DW_AT_name | grep -m 1 'test/format')
    
    # TODO Replace reliance bash regex support for old school
    # pipes and awk. *sigh*
    #
    pat=' (\S+)/test/format/\S+\.c$'
    if [[ $line =~ $pat ]]; then
        build_src_root=${BASH_REMATCH[1]}
        solib_dir=$(find $artifacts_dir -type d -name 'cmake_build')

        cat<<EOF>$gdbinit
set solib-search-path $solib_dir
set substitute-path $build_src_root $src_dir
EOF
        echo "Created $gdbinit"
    fi
fi


# Modify .bashrc to make WT debugging easier by adding the location
# of the WT shared object to LD_LIBRARY_PATH. Add some common developer
# "finger memory" shell aliases, and a whimisical convenience alias to
# jump to the root of the unpacked artifacts.
#
# The BEGIN and END markers emulate markers already left
# in the file by Evergreen (maybe Ansible)?
#
if ! grep '^#(BEGIN|END) WT DEBUG' $HOME/.bashrc ; then
    cp $HOME/.bashrc $HOME/evergreen.bashrc

    # TODO Add path to libtcmalloc.so if it is present.
    cat<<EOF>>$HOME/.bashrc
# BEGIN WT DEBUG
export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:$artifacts_dir/cmake_build

alias l='\ls'
alias ll='\ls -lAh'
alias spelunk='cd $artifacts_dir/cmake_build'
# END WT DEBUG
EOF
    echo "Setup LD_LIBRARY_PATH for debugging."
else
    echo "Looks like LD_LIBRARY_PATH already setup for debugging."
fi
