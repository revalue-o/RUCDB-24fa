#!/bin/bash

# 读取 YAML 文件
parse_yaml() {
   local prefix=$2
   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
   sed -ne "s|^\($s\)\($w\)$s:$s\"\(.*\)\"$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  $1 |
   awk -F$fs '{
      indent = length($1)/2;
      vname[indent] = $2;
      for (i in vname) {if (i > indent) {delete vname[i]}}
      if (length($3) > 0) {
         vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
         printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
      }
   }'
}
eval $(parse_yaml S2Z.yaml "config_")

# 拉取镜像
#docker pull $config_IMAGE_NAME

# 运行容器
docker run  \
  --privileged=true \
  -d \
  --gpus all \
  --shm-size 64g \
  -p 8081:80 \
  -v $config_BAREMETAL_DIR:$config_SHARE_DIR \
  --name $config_CONTAINER_NAME \
  $config_IMAGE_NAME \
  --model-id $config_MODEL_DIR \
  --num-shard $config_NUM_GPUS
  


