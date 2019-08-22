a=20000
while  [[ $a -ne 0 ]]
do
echo $a
a=`echo $a - 1 | bc`
done
