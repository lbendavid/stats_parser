png_file_1=var."/stat_poste_plm_usage.png"
png_file_2=var."/stat_poste_plm.png"
#data_file="stat_plm_usage.dat"
x_label="poste"
y_label="nombre de lancements"

set title "Lancement lanceurs PLM 2018-2019"
set style data histograms
set style fill solid
set xlabel "nombre de lancements par tranche"
set ylabel "nombre de poste dans la catégorie"
set terminal png
set output png_file_1
plot data_file i 1 using 2:xtic(1) title columnheader(1)
set terminal x11
replot
reset
set terminal x11
pause -1
set style data line
set autoscale
set title "Classement des postes lancement 2018-2019"
set xlabel x_label
set ylabel y_label
set terminal png
set output png_file_2
plot data_file i 0 using 1:2 with line linewidth 5 title columnheader(1), \
     data_file i 0 using 1:3 with points title "3DExp", \
     data_file i 0 using 1:4 with points title "V6", \
     data_file i 0 using 1:5 with points title "V5"
set terminal x11
replot
pause -1
reset