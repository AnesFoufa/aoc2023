cat ../input.txt | sed 's/[^0-9]//g'| sed -n 's/^\(.\)\(.*\)\(.\)$/\1\3/p; /^.$/s/^\(.\)$/\1\1/p' | paste -sd+ | bc
