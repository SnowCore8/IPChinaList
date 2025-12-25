import requests
from lxml import etree
import time
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def init_yaml_file():
    """
    初始化文件，写入头部信息
    """
    try:
        with open("china_asn.txt", "w", encoding="utf-8") as asn_file:
            pass
        logging.info("TXT 文件已初始化")
    except Exception as e:
        logging.error(f"初始化 TXT 文件失败: {e}")

    try:
        with open("china_asn_mihomo.yaml", "w", encoding="utf-8") as asn_file:
            asn_file.write("payload:\n")
        logging.info("YAML 文件已初始化")
    except Exception as e:
        logging.error(f"初始化 YAML 文件失败: {e}")

def fetch_asn_data(url, headers, max_retries=3):
    """
    获取 ASN 数据
    """
    for _ in range(max_retries):
        try:
            logging.info(f"正在从 {url} 获取 ASN 数据...")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("数据获取成功")
            return response.text
        except requests.exceptions.RequestException as e:
            logging.warning(f"请求失败: {e}, 正在重试...")
            time.sleep(2)
    logging.error("达到最大重试次数，获取数据失败")
    return None

def parse_asn_data(html):
    """
    解析 ASN 数据
    """
    try:
        logging.info("正在解析 ASN 数据...")
        tree = etree.HTML(html)
        # 根据提供的 HTML 结构调整 XPath 表达式
        asns = tree.xpath('//tr[td/a[starts-with(@href, "/AS")]]')
        logging.info(f"提取到 {len(asns)} 条 ASN 数据")
        return asns
    except Exception as e:
        logging.error(f"解析 ASN 数据时出错: {e}")
        return []

def save_asn_to_yaml(asns):
    """
    将 ASN 数据保存到 YAML 文件
    """
    if not asns:
        logging.info("没有 ASN 数据可保存")
        return
    
    try:
        logging.info("正在将 ASN 数据保存到 TXT 文件...")
        with open("china_asn.txt", "a", encoding="utf-8") as asn_file:
            for asn in asns:
                # 提取 ASN 号码和名称
                asn_number = asn.xpath('.//td[1]/a/text()')
                asn_name = asn.xpath('.//td[2]/text()')
                
                if asn_number and asn_name:
                    asn_number = asn_number[0].replace('AS', '')
                    asn_name = asn_name[0].strip()
                    
                    asn_info = f"{asn_number} # {asn_name}"
                    asn_file.write(asn_info + "\n")
        logging.info("ASN 数据已成功保存到 china_asn.txt 文件中")
        
        logging.info("正在将 ASN 数据保存到 YAML 文件...")
        with open("china_asn_mihomo.yaml", "a", encoding="utf-8") as asn_file:
            for asn in asns:
                # 提取 ASN 号码和名称
                asn_number = asn.xpath('.//td[1]/a/text()')
                asn_name = asn.xpath('.//td[2]/text()')
                
                if asn_number and asn_name:
                    asn_number = asn_number[0].replace('AS', '')
                    asn_name = asn_name[0].strip()
                    
                    asn_info = f"  - IP-ASN,{asn_number} # {asn_name}"
                    asn_file.write(asn_info + "\n")
        logging.info("ASN 数据已成功保存到 china_asn_mihomo.yaml 文件中")
    except Exception as e:
        logging.error(f"保存 ASN 数据时出错: {e}")

def main():
    url = "https://bgp.he.net/country/CN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    
    init_yaml_file()
    html = fetch_asn_data(url, headers)
    
    if html:
        asns = parse_asn_data(html)
        save_asn_to_yaml(asns)

if __name__ == "__main__":
    main()
