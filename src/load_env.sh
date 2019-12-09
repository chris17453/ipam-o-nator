#!/bin/bash

printf "\nBAM URL:"
read bam_url

printf "\nBAM Account:"
read bam_account


printf "\nBAM Password:"
read bam_pass


export BAM_ACCOUNT=$bam_account
export BAM_PASSWORD=$bam_pass
export BAM_URL=$bam_url

