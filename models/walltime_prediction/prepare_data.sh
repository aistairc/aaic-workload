#! /bin/bash

REGISTRY_URL=https://github.com/aistairc/aaic-workload
WORKLOAD_GZ_REMOTE_PATH=workloads/quarter/2018/aaicwl-2018Q1.csv.gz
WORKLOAD_GZ_LOCAL_PATH=${WORKLOAD_GZ_REMOTE_PATH##*/}
WORKLOAD_FILE=${WORKLOAD_GZ_LOCAL_PATH%.*}

dvc get $REGISTRY_URL $WORKLOAD_GZ_REMOTE_PATH
gunzip $WORKLOAD_GZ_LOCAL_PATH
mv $WORKLOAD_FILE ${WORKLOAD_FILE}.bk
sed 's/, /,/g' ${WORKLOAD_FILE}.bk > $WORKLOAD_FILE
rm ${WORKLOAD_FILE}.bk
