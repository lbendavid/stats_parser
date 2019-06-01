basename="stat_juniper"
data_file=basename.".dat"
pc_png=basename."_pc.png"
user_png=basename."_user.png"
histo_png=basename."_histo.png"
start="15/02/2019"
stop="24/05/2019"
set title "PC usage VPN du ".start." ".stop
set autoscale
print data_file

set xlabel "pc par taux d'usage"
set ylabel "Nombre d'heures d'utilisation"
set y2label "Nombre d'utilisateur different pour le pc"
set y2tics
set yrange [0:50]
set terminal png
set output pc_png
set key autotitle columnheader
plot data_file i 0 using 1:2 with line linewidth 1 linecolor 'black'axes x1y1, \
     data_file i 0 using 1:4 with line linewidth 1 linecolor 'red' axes x1y1, \
     data_file i 0 using 1:3 with points ls 2 linecolor 'magenta' axes x1y2
set terminal x11
replot
reset
pause -1
set style data line
set title "User usage VPN du ".start." ".stop
set xlabel "Users par taux d'usage"
set y2label "Nombre de devices utilisés dans la période"
set yrange [0:50]
set terminal png
set output user_png
set key autotitle columnheader
set y2tics
plot data_file i 1 using 1:2 with line linewidth 1 linecolor 'black' axes x1y1, \
     data_file i 1 using 1:4 with line linewidth 1 linecolor 'red' axes x1y1, \
     data_file i 1 using 1:3 with points ls 2 linecolor 'magenta' axes x1y2
set terminal x11
replot
pause -1

reset
set terminal png
set output user_png
set autoscale
set style data histograms
set style histogram clustered gap 1
set style fill solid
set xtics rotate by 90 offset character 0, -1, 0 autojustify
set xlabel "bloc max d'heures d'usage du pc"
set ylabel "nombre de devices dans le bloc"
set grid y
set key outside bottom horizontal
set key autotitle columnheader
plot data_file i 2 using 2:xtic(1)
set terminal x11
replot
pause -1