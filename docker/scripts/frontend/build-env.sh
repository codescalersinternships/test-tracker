#!/bin/sh

set -ex
values="
window.env = {
  SERVER_DOMAIN_NAME_API: '$SERVER_DOMAIN_NAME_API',
  GITHUB_CLIENT_ID: '$GITHUB_CLIENT_ID',
  GITHUB_CLIENT_SECRET: '$GITHUB_CLIENT_SECRET',

};
"
# decide the config file path
file="/usr/share/nginx/html/config.js"
echo $values > $file
echo -e "\e[1;32m$values"

echo "++++++++++++++++++++++++++++++++++++++++++++"
echo "file=$file"
echo "++++++++++++++++++++++++++++++++++++++++++++"
