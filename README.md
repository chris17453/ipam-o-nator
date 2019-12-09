# IPAM-O-NATOR
- Simple bluecat addressmanager interface  and automation hooks in a container

## what it does
- export / importing of dns data

- This is a simple web ui that generates BLOCK and SUBNETS
- BLOCKS can contain BLOCKS
- BLOCKS can contain SUBNETS
- BLOCKS can be nested
- This tool validates data from a paste entry from a spreadsheet
- preforms preflight summarys
- option to dry run with command summary
- gives postflight summarys
- imports data
- exports data
- export summary contains the actual commands used to generate the update 
- has a transaction log

## configure ldap
```bash
make ldap endpoint
```

## build
- to build the contiainer
```bash
make build
```

## run
- to run the container
```bash
make run
```

## debug
- to run the container for testing without a docker
```bash
make debug
```


## Docker repository upload
- this will push the image to a docker repository of your chosing
- defaults editable in make file
```bash
make push
```

## Create new Open Shift Project
```bash
make deploy-new-openshift
```

## Update Open Shift Project
```bash
make deploy-update-openshift
```
