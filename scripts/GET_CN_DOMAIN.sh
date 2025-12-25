#!/bin/bash

file1=tmp.txt
file2=old.txt
file3=china_domain.txt
file4=china_domain_mihomo.yaml

echo "- 转换 txt 规则..."
curl -sSL https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/refs/heads/release/china-list.txt > $file2
curl -sSL https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cn.list |sed 's/^\+\.//g' >> $file2
sed -i "s/^/\+\./g" $file2
cat $file2 |sort |uniq >$file3

echo "- 转换 yaml 规则..."
curl -sSL https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/refs/heads/release/china-list.txt |sed "s/^/  - \+\./g" > $file2
curl -sSL https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cn.list |sed "s/^\+\./  - \*\./g" >> $file2
sed -i "s/- /- '/g" $file2
sed -i "s/$/\'/g" $file2
echo 'payload:' >$file4
cat $file2 |sort |uniq >>$file4

rm -f $file1 $file2
