import requests
import math

# 下载APNIC的IP数据库文件
def download_apnic_data():
    url = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    response = requests.get(url)
    if response.status_code == 200:
        with open('apnic.txt', 'wb') as f:
            f.write(response.content)
        print("APNIC数据已成功下载到apnic.txt文件中")
    else:
        print("下载APNIC数据失败，状态码：", response.status_code)
        return None
    return 'apnic.txt'

# 筛选中国的IPv4和IPv6地址段并保存到txt文件
def filter_and_save_china_ips(apnic_file):
    ipv4_blocks = []
    ipv6_blocks = []
    with open(apnic_file, 'r') as infile:
        for line in infile:
            parts = line.strip().split('|')
            if len(parts) >= 5 and parts[0] == 'apnic' and parts[1] == 'CN':
                if parts[2] == 'ipv4':
                    network_address = parts[3]
                    ip_count = int(parts[4])
                    prefix_length = 32 - int(math.log2(ip_count))
                    cidr_block = f"{network_address}/{prefix_length}"
                    ipv4_blocks.append(cidr_block)
                elif parts[2] == 'ipv6':
                    network_address = parts[3]
                    prefix_length = parts[4]
                    cidr_block = f"{network_address}/{prefix_length}"
                    ipv6_blocks.append(cidr_block)

    # 保存IPv4地址段到txt文件
    with open('china_ipv4.txt', 'w') as ipv4_file:
        for block in ipv4_blocks:
            ipv4_file.write(block + '\n')
    print("中国的IPv4地址段已成功保存到china_ipv4.txt文件中")

    # 保存IPv6地址段到txt文件
    with open('china_ipv6.txt', 'w') as ipv6_file:
        for block in ipv6_blocks:
            ipv6_file.write(block + '\n')
    print("中国的IPv6地址段已成功保存到china_ipv6.txt文件中")

    # 生成mihomo的yaml规则
    generate_mihomo_yaml(ipv4_blocks, ipv6_blocks)

# 生成mihomo的yaml规则
def generate_mihomo_yaml(ipv4_blocks, ipv6_blocks):
    # 生成IPv4的yaml规则
    with open('china_ipv4_mihomo.yaml', 'w') as ipv4_yaml_file:
        ipv4_yaml_file.write("payload:\n")
        for block in ipv4_blocks:
            ipv4_yaml_file.write(f"  - IP-CIDR,{block}\n")
    print("中国的IPv4地址段已成功生成mihomo的yaml规则到china_ipv4_mihomo.yaml文件中")

    # 生成IPv6的yaml规则
    with open('china_ipv6_mihomo.yaml', 'w') as ipv6_yaml_file:
        ipv6_yaml_file.write("payload:\n")
        for block in ipv6_blocks:
            ipv6_yaml_file.write(f"  - IP-CIDR6,{block}\n")
    print("中国的IPv6地址段已成功生成mihomo的yaml规则到china_ipv6_mihomo.yaml文件中")

if __name__ == "__main__":
    apnic_file = download_apnic_data()
    if apnic_file:
        filter_and_save_china_ips(apnic_file)
