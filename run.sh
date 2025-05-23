#!/bin/bash

show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -h, --help        Show this help message and exit"
    echo "  -o, --ori         Origin cell number (default: 4)"
    echo "  -n, --max_num     Maximum simulate number (default: 1000)"
    echo "  -s, --sample      Sample name (default: 0)"
    echo "  -c, --dis_shape   Displacement shape (default: hex)"
    echo "  -t, --max_t       Maximum time (default: 10000)"
    echo "  -O, --out_dir     Output directory (default: tumopp_test_{sample})"
    echo "  -D, --dim         Dimension (default: 3)"
    echo "  -L, --lattice     Lattice type (default: linear)"
    echo "  -k, --shape_param  Shape parameter of waiting time distribution for cell division (default:1.0)"
    echo "  -b, --birth_prob  Birth probability (default: 0.5)"
    echo "  -d, --death_prob  Death probability (default: 0.1)"
    echo "  -m, --move_prob   Move probability (default: 0.1)"
    echo "  -v, --verbose     Verbose output (default: 0)"
    echo "  -M, --more        More verbose help"
    exit 0
}

# Default values
ori=4
max_num=1000
sample=0
dis_shape="hex"
max_t=10000
dim=3
lattice="linear"
shape_param=1.0
birth_prob=0.5
death_prob=0.1
move_prob=0.1
verbose=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            ;;
        -M|--more)
            tumopp -h
            exit 0
            ;;
        -o|--ori)
            ori="$2"
            shift
            ;;
        -n|--max_num)
            max_num="$2"
            shift
            ;;
        -s|--sample)
            sample="$2"
            shift
            ;;
        -c|--dis_shape)
            dis_shape="$2"
            shift
            ;;
        -t|--max_t)
            max_t="$2"
            shift
            ;;
        -O|--out_dir)
            out_dir="$2"
            shift
            ;;
        -D|--dim)
            dim="$2"
            shift
            ;;
        -L|--lattice)
            lattice="$2"
            shift
            ;;
        -k|--shape_param)
            shape_param="$2"
            shift
            ;;
        -b|--birth_prob)
            birth_prob="$2"
            shift
            ;;
        -d|--death_prob)
            death_prob="$2"
            shift
            ;;
        -m|--move_prob)
            move_prob="$2"
            shift
            ;;
        -v|--verbose)
            verbose="$2"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
    shift
done

# Set default output directory if not provided
if [ -z "$out_dir" ]; then
    out_dir="tumopp_test${sample}"
fi

tumopp -O $ori -D $dim -L $lattice -N $max_num -C $dis_shape -k $shape_param -b $birth_prob -d $death_prob -m $move_prob --max_time $max_t -o $out_dir
zcat ./$out_dir/population.tsv.gz > ./$out_dir/population.tsv
python trace.py $ori $out_dir
python plot3D.py $out_dir
python tree.py $ori $out_dir $verbose