import configparser
cp = configparser.ConfigParser()  # 配置文件解析工具
cp.read('config.ini')


class Config:
    @staticmethod
    def get_configs():
        id_c = pwd_c = ''  # 最开始设置为空
        if cp.has_section('user'):
            if cp.has_option('user', 'id'):
                id_c = cp.get('user', 'id')
            if cp.has_option('user', 'pwd'):
                pwd_c = cp.get('user', 'pwd')
        else:
            cp.add_section('user')
            cp.set('user', 'id', '')
            cp.set('user', 'pwd', '')
        return id_c, pwd_c

    @staticmethod
    def set_id_c(n_id):
        cp.set('user', 'id', n_id)
        cp.write(open('config.ini', 'w'))

    @staticmethod
    def set_pwd_c(n_pwd):
        cp.set('user', 'pwd', n_pwd)
        cp.write(open('config.ini', 'w'))

