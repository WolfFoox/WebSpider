# 设置异常捕获机制==》做出一个装饰器函数
'''
 闭包的构成
    1.必须是一个嵌套函数
    2.内函数必须使用外函数的非全局变量
    3.外函数的返回值必须是内涵上的函数名
'''
from retrying import retry
def get_error(n): # n用来接收业务函数名
    f = open(r'error.txt','w+',encoding='utf-8')
    def exception_handing(*args, **kwargs): # 这里是接收业务函数的参数
        try:
            res = n(*args, **kwargs) # 被装饰函数的真正调用语句
            status_code = res.status_code
        except Exception as e: # 捕获到异常进行对应的处理

            try:
                # 设置重试机制处理可恢复的异常
                @retry(stop_max_attempt_number = 3,wait_random_min=1000,wait_random_max=3000)
                def time_retry():
                    return n(*args, **kwargs) # kwargs = {'url':url_list}
            except Exception as e:
                f.write(f'{kwargs["url"]}请求失败,错误信息为:{repr(e)};\n')
            else:
                f.write(f'{kwargs["url"]}请求成功，响应状态为:{time_retry().status_code};\n')
        else:
            # 写入状态码
            f.write(f'{kwargs["url"]}请求成功，响应状态为:{status_code};\n')
        finally:
            f.flush() # 把write保存
            return res    # 这里才是真的把响应数据返回给调度器
    return exception_handing