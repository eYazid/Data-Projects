#! /bin/bash

city=Casablanca
curl -s wttr.in/$city?T --output weather_report

obs_temp_min=$(head -7 weather_report | grep '°' | grep -Eo -e '-?[[:digit:]].*' | tr -d ')°C' | cut -d '(' -f1 )
obs_temp_max=$(head -7 weather_report | grep '°' | grep -Eo -e '-?[[:digit:]].*' | tr -d ')°C' | cut -d '(' -f2 )

fc_temp_min=$(curl -s wttr.in/$city?T | head -23 | tail -1 | grep '°' | cut -d 'C' -f2 | grep -Eo -e '-?[[:digit:]].*' | tr -d ')°C' | cut -d '(' -f1)
fc_temp_min=$(curl -s wttr.in/$city?T | head -23 | tail -1 | grep '°' | cut -d 'C' -f2 | grep -Eo -e '-?[[:digit:]].*' | tr -d ')°C' | cut -d '(' -f2)

accuracy=$(($fc_temp_min - $obs_temp_min))

if [[ -1 -le $accuracy ]] && [ $accuracy -le 1 ]
then
   accuracy_range=excellent
elif [ -2 -le $accuracy ] && [ $accuracy -le 2 ]
then
    accuracy_range=good
elif [ -3 -le $accuracy ] && [ $accuracy -le 3 ]
then
    accuracy_range=fair
else
    accuracy_range=poor
fi


TZ='Morocco/Casablanca'
	
day=$(TZ='Morocco/Casablanca' date -u +%d) 
month=$(TZ='Morocco/Casablanca' date +%m)
year=$(TZ='Morocco/Casablanca' date +%Y)

record=$(echo -e "$year\t$month\t$day\t$obs_temp_min\t$fc_temp_min\t$accuracy_range")
echo $record>>rx_poc.log



