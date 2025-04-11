import paramiko
import os
from stat import S_ISDIR
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file_via_sftp():
    """
    通过SFTP从远程服务器下载city.json文件
    """
    # 服务器配置
    host = '47.109.99.60'
    port = 22
    username = 'root'
    # 私钥路径需要用户提供 (确保路径没有引号)
    private_key_path = r'C:\Users\23717\Downloads\jjhadjhuidhuajdfkslndspajklngiyasdnaxjsa.pem'  # 请替换为实际私钥路径
    if not os.path.exists(private_key_path):
        raise FileNotFoundError(f"私钥文件不存在: {private_key_path}")
    remote_path = '/root/CtripSpider/city.json'
    local_path = os.path.join(os.path.dirname(__file__), 'city.json')

    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 使用私钥连接 - 需要用户提供私钥
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        ssh.connect(host, port, username, pkey=private_key)

        # 创建SFTP客户端
        sftp = ssh.open_sftp()

        # 下载文件
        sftp.get(remote_path, local_path)
        logger.info(f"文件已成功下载到: {local_path}")

        # 关闭连接
        sftp.close()
        ssh.close()

    except Exception as e:
        logger.error(f"文件下载失败: {str(e)}")
        raise

if __name__ == '__main__':
    download_file_via_sftp()
