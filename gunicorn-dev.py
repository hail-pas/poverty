from gevent import monkey

monkey.patch_all()
bind = '0.0.0.0:8000'
daemon = False
worker_class = 'gevent'
accesslog = '-'  # 访问日志文件，'-' 表示标准输出
errorlog = '-'  # 错误日志文件，'-' 表示标准输出
# 最大请求数之和重启worker，防止内存泄漏
max_requests = 4096
# 随机重启防止所有worker一起重启：randint(0, max_requests_jitter)
max_requests_jitter = 512
