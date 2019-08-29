import paramiko
# 创建SSH对象

ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def opr(ssh, os_type, host):
    commands_centos = ('yum install curl -y', 'curl -sS https://get.docker.com/ | sh',
        'service docker restart', 'docker run --restart=always hello-world')

    commands_debian_or_ubuntu = ('apt-get install curl -y', 'curl -sS https://get.docker.com/ | sh',
        'systemctl enable docker.service', 'systemctl start docker.service',
        'docker run --restart=always hello-world')

    commands = [commands_centos, commands_debian_or_ubuntu]

    for command in commands[os_type]:

        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        res,err = stdout.read().decode(),stderr.read().decode()

        print(command)
        print('Info:', res)

        if err:
            print(host, 'Error:', err)
            break
    else:
        print('%s finished!' % host)

with open('namepw.txt','r') as f:
    for line in f:
        print()
        params = line.split(',')
        params = [p.strip() for p in params]
        print(params)

        # 连接服务器
        ssh.connect(hostname=params[0], port=22, username=params[1], password=params[2])
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command('cat /etc/os-release')
        # 获取命令结果
        res,err = stdout.read().decode(),stderr.read().decode()

        if err:
            print('Login Error:',err)
            continue
        else:
            print(res)
            if 'centos' in res.lower():
                os_type = 0
            else:
                os_type = 1
            opr(ssh, os_type, params[0])

    # 关闭连接
    ssh.close()