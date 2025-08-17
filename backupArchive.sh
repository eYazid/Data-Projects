#!/bin/bash

# This checks if the number of arguments is correct
# If the number of arguments is incorrect ( $# != 2) print error message and exit
if [[ $# != 2 ]]
then
  echo "backup.sh target_directory_name destination_directory_name"
  exit
fi

# This checks if argument 1 and argument 2 are valid directory paths
if [[ ! -d $1 ]] || [[ ! -d $2 ]]
then
  echo "Invalid directory path provided"
  exit
fi

targetDirectory=$1
destinationDirectory=$2

echo "$targetDirectory"
echo "$destinationDirectory"


currentTS=$(date +"%Y-%m-%dT%H:%M:%S")


backupFileName="backup-$currentTS.tar.gz"

origAbsPath="$pwd"

cd $destinationDirectory
destDirAbsPath="$pwd"

cd ..
cd $targetDirectory

yesterdayTS=$(($currentTS - 24 * 60 * 60))

declare -a toBackup
files=(*)
for file in $files
do
  file_last_modified_date=$(date -r $file +%s)
  if [[ $file_last_modified_date -gt $yesterdayTS ]]
  then
    toBackup+=($file)
  fi
done

tar -czvf $backupFileName ${toBackup[@]}

mv $backupFileName $destDirAbsPath
