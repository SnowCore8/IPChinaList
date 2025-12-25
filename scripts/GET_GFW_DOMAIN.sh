#!/bin/bash

file1=tmp.txt
file2=old.txt
file3=gfw_domain.txt
file4=gfw_domain_mihomo.yaml

# 下载GFWList并转换为Clash规则
echo "- 正在下载GFWList..."
curl -sSl https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt |base64 -d > $file1

# grep '[0-9]\{0,3\}\.[0-9]\{0,3\}\.[0-9]\{0,3\}\.[0-9]\{0,3\}' $file1

echo "- 正在处理规则..."
echo "- 处理注释..."
sed -i '/^\!/d' $file1
sed -i '/^\[/d' $file1
echo "- 处理白名单..."
sed -i '/^\@\@/d' $file1
echo "- 处理黑名单..."
sed -i '/^\|https:\/\//d' $file1
sed -i '/^\|http:\/\//d' $file1
echo "- 处理协议..."
sed -i 's/^https\:\/\///g' $file1
sed -i 's/^http\:\/\///g' $file1
echo "- 处理后缀..."
sed -i 's/\/.*//g' $file1

echo "- 转换 txt 规则..."
grep '^\.' $file1 |sed 's/^\.//g' > $file2
grep '^|\|' $file1 |sed 's/^\|\|//g' >> $file2
grep '^\|\*' $file1 |sed 's/^\|\*/\*/g' >> $file2
curl -sSL https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/refs/heads/release/gfw.txt >> $file2
curl -sSL https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/gfw.list |sed 's/^\+\.//g' >> $file2
sed -i "s/^/\+\./g" $file2
cat $file2 |sort |uniq >$file3

echo "- 转换 yaml 规则..."
grep '^\.' $file1 |sed "s/^\./  - +\./g" > $file2
grep '^\|\|' $file1 |sed "s/^\|\|/  - +\./g">> $file2
curl -sSL https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/refs/heads/release/gfw.txt |sed "s/^/  - \+\./g" >> $file2
curl -sSL https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/gfw.list |sed "s/^\+\./  - /g" >> $file2
sed -i "s/- /- '/g" $file2
sed -i "s/$/\'/g" $file2
echo 'payload:' >$file4
cat $file2 |sort |uniq >>$file4

rm -f $file1 $file2
