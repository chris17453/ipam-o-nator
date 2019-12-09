#!/bin/bash

printf "\nBAM URL:"
read bam_url

printf "\nBAM Account:"
read bam_account


printf "\nBAM Password:"
read bam_pass


echo $bam_account>./deployment/config.txt
echo $bam_pass>>./deployment/config.txt
echo $bam_url>>./deployment/config.txt

