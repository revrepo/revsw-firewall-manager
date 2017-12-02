#!/bin/bash
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEMPLATE_DIR=$BASE_DIR"/templates"
OUTPUT_DIR="/etc/puppet/modules/firewall/files/ufw_firewall_scripts"

for template in `ls -1 $TEMPLATE_DIR`; do
    result_file=`basename -s .jinja $template`.sh
    $BASE_DIR/server_list_jinja.py $TEMPLATE_DIR/$template $OUTPUT_DIR/$result_file
    chmod a+x $OUTPUT_DIR/$result_file
done

