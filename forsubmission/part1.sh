#!/bin/sh

# set up
mkdir forsubmission_auto

move_with_name()
{
    name_prefix=$1

    config_suffix="config.ini"
    stats_suffix="stats.txt"
    submission_dir="forsubmission_auto"

    from_loc_config="m5out/config.ini"
    from_loc_stats="m5out/stats.txt"

    to_loc_config="$submission_dir/$name_prefix$config_suffix"
    to_loc_stats="$submission_dir/$name_prefix$stats_suffix"

    mv $from_loc_config $to_loc_config
    mv $from_loc_stats $to_loc_stats
}

# number 1
build/X86/gem5.opt configs/tutorial/simple.py --cpu_model=1
move_with_name 1_simple_timingsimplecpu_

# number 2
build/X86/gem5.opt configs/tutorial/simple.py --cpu_model=2
move_with_name 2_simple_minorcpu_


# number 3
cache_for_3="--use_cache=1 --l1i_size=32kB --l1i_assoc=1 --l1d_size=64kB --l1d_assoc=1 --l2_size=4MB --l2_assoc=8"
build/X86/gem5.opt configs/tutorial/simple.py --cpu_model=2 $cache_for_3
move_with_name 3_cached_minorcpu_

# number 4
number_4()
{
    nbr=$1; shift
    mem_conf=$1
    configs=$*
    undscr="_"

    for i in '1GHz' '1.5GHz' '2GHz' '2.5GHz' '3GHz'
    do
        build/X86/gem5.opt configs/tutorial/simple.py --cpu_model=1 --clk_freq=$i $configs
        cpu="timingcpu"
        move_with_name $nbr$undscr$mem_conf$undscr$cpu$undscr$i$undscr

        build/X86/gem5.opt configs/tutorial/simple.py --cpu_model=2 --clk_freq=$i $configs
        cpu="minorcpu"
        move_with_name $nbr$undscr$mem_conf$undscr$cpu$undscr$i$undscr
    done
}

# number 4 through 8
number_4_through_8()
{
    nth=""
    ddr3_2133="--mem_config=DDR3_2133_8x8"
    ddr2="--mem_config=LPDDR2_S4_1066_1x32"
    for mem_config in $nth $ddr3_2133 $ddr2
    do
        number_4 4 $mem_config
        
        # number 5
        number_4 5 $mem_config $cache_for_3
        
        # number 6
        cache_for_6="--use_cache=1 --l1i_size=32kB --l1i_assoc=2 --l1d_size=64kB --l1d_assoc=2 --l2_size=4MB --l2_assoc=8"
        number_4 6 $mem_config $cache_for_6
        
        # number 7
        cache_for_7="--use_cache=1 --l1i_size=64kB --l1i_assoc=1 --l1d_size=128kB --l1d_assoc=1 --l2_size=4MB --l2_assoc=8"
        number_4 7 $mem_config $cache_for_7

    done
}

number_4_through_8

# finally move to git repo
rm -rf configs/tutorial/forsubmission_auto
mv forsubmission_auto configs/tutorial/
