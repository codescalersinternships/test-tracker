#!/bin/sh

set -ex
values="
window.env = {
  SERVER_DOMAIN_NAME_API: '$SERVER_DOMAIN_NAME_API',
};
"
# decide the config file path
file="/usr/share/nginx/html/config.js"
echo $values > $file
echo -e "\e[1;32m$values"

echo "++++++++++++++++++++++++++++++++++++++++++++"
echo "file=$file"
echo "++++++++++++++++++++++++++++++++++++++++++++"
