import requests
import math
import logging

# 设置日志配置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 下载APNIC的IP数据库文件
def download_apnic_data():
    url = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    response = requests.get(url)
    if response.status_code == 200:
        with open('apnic.txt', 'wb') as f:
            f.write(response.content)
        logging.info("APNIC数据已成功下载到apnic.txt文件中")
    else:
        logging.error("下载APNIC数据失败，状态码：", response.status_code)
        return None
    return 'apnic.txt'

# 筛选中国的IPv4和IPv6地址段并保存到txt文件
def filter_and_save_china_ips(apnic_file):
    asn_blocks = []
    ipv4_blocks = []
    ipv6_blocks = []
    with open(apnic_file, 'r') as infile:
        for line in infile:
            parts = line.strip().split('|')
            if len(parts) >= 5 and parts[0] == 'apnic' and parts[1] == 'CN':
                if parts[2] == 'asn':
                    asn_address = parts[3]
                    asn_block = f"{asn_address}"
                    asn_blocks.append(asn_block)
                elif parts[2] == 'ipv4':
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

    # 保存ASN到txt文件
    with open('china_asn.txt', 'w') as asn_file:
        for block in asn_blocks:
            asn_file.write(block + '\n')
    logging.info("中国的ASN已成功保存到china_asn.txt文件中")

    # 保存IPv4地址段到txt文件
    with open('china_ipv4.txt', 'w') as ipv4_file:
        for block in ipv4_blocks:
            ipv4_file.write(block + '\n')
    logging.info("中国的IPv4地址段已成功保存到china_ipv4.txt文件中")

    # 保存IPv6地址段到txt文件
    with open('china_ipv6.txt', 'w') as ipv6_file:
        for block in ipv6_blocks:
            ipv6_file.write(block + '\n')
    logging.info("中国的IPv6地址段已成功保存到china_ipv6.txt文件中")

    # 保存IPv4&IPv6地址段到txt文件
    with open('china_ip.txt', 'w') as ip_file:
        for block in ipv4_blocks + ipv6_blocks:
            ip_file.write(block + '\n')
    logging.info("中国的IPv4&IPv6地址段已成功保存到china_ip.txt文件中")

    # 生成mihomo的txt规则
    generate_mihomo_yaml(asn_blocks, ipv4_blocks, ipv6_blocks)

# 生成mihomo的yaml规则
def generate_mihomo_yaml(asn_blocks, ipv4_blocks, ipv6_blocks):
    # 生成ASN的yaml规则
    with open('china_asn_mihomo.yaml', 'w') as asn_yaml_file:
        asn_yaml_file.write("payload:\n")
        for block in asn_blocks:
            asn_yaml_file.write(f"  - 'IP-ASN,{block}'\n")
    logging.info("中国的ASN已成功生成mihomo的yaml规则到china_asn_mihomo.yaml文件中")

    # 生成IPv4的yaml规则
    with open('china_ipv4_mihomo.yaml', 'w') as ipv4_yaml_file:
        ipv4_yaml_file.write("payload:\n")
        for block in ipv4_blocks:
            ipv4_yaml_file.write(f"  - 'IP-CIDR,{block}'\n")
    logging.info("中国的IPv4地址段已成功生成mihomo的yaml规则到china_ipv4_mihomo.yaml文件中")

    # 生成IPv6的yaml规则
    with open('china_ipv6_mihomo.yaml', 'w') as ipv6_yaml_file:
        ipv6_yaml_file.write("payload:\n")
        for block in ipv6_blocks:
            ipv6_yaml_file.write(f"  - 'IP-CIDR6,{block}'\n")
    logging.info("中国的IPv6地址段已成功生成mihomo的yaml规则到china_ipv6_mihomo.yaml文件中")

    # 生成IPv4&IPv6的yaml规则
    with open('china_ip_mihomo.yaml', 'w') as ip_yaml_file:
        ip_yaml_file.write("payload:\n")
        for block in ipv4_blocks + ipv6_blocks:
            ip_yaml_file.write(f"  - 'IP-CIDR,{block}'\n")
    logging.info("中国的IPv4&IPv6地址段已成功生成mihomo的yaml规则到china_ip_mihomo.yaml文件中")

    # 生成ASN&IPv4&IPv6的yaml规则
    with open('china_mihomo.yaml', 'w') as cn_yaml_file:
        cn_yaml_file.write("payload:\n")
        for block in asn_blocks:
            cn_yaml_file.write(f"  - 'IP-ASN,{block}'\n")
        for block in ipv4_blocks + ipv6_blocks:
            cn_yaml_file.write(f"  - 'IP-CIDR,{block}'\n")
    logging.info("中国的ASN&IPv4&IPv6地址段已成功生成mihomo的yaml规则到china_mihomo.yaml文件中")

if __name__ == "__main__":
    apnic_file = download_apnic_data()
    if apnic_file:
        filter_and_save_china_ips(apnic_file)
