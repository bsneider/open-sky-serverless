#!/bin/bash
AWSPROFILE=$1

# download file
echo 'download file if not exists'
FILE=./src/terraform/modules/s3/external/flightlist_20190101_20190131.csv.gz
[ -f $FILE ] && echo "$FILE exists." || curl --progress-bar "https://zenodo.org/record/5377831/files/flightlist_20190101_20190131.csv.gz?download=1" -o $FILE

# cd into terraform folder
echo 'cd into tf folder'
cd ./src/terraform
echo $PWD

# terraform apply yourself
echo 'terraform init'
terraform init
echo 'terraform apply'
terraform apply -auto-approve #-var profile=”$AWSPROFILE”
echo 'curl the url'
URL=`terraform output | grep -Eo 'https://[^ >]+' | sed 's/.$//'`
echo $URL
for i in {1..10} 
do 
    curl -X GET $URL/report
    echo '\n'
    sleep 2
done