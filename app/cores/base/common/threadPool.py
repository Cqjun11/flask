from concurrent.futures import ThreadPoolExecutor, as_completed

class ThreadPool:
    def __init__(self):
        self.max_workers = 10
        self.executor = None

    def start(self):
        """ 启动线程池"""
        if self.executor is None:
            self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        else:
            print("线程池已启动")

    def stop(self):
        """关闭线程池"""
        if self.executor is not None:
            self.executor.shutdown(wait=True)
            self.executor = None
        else:
            print("线程池已关闭或未启动")

    def submit_task(self, func, *args, **kwargs):
        """提交任务到线程池"""
        if self.executor is None:
            print("线程池未启动，请先启动线程池")
            self.start()
        future = self.executor.submit(func, *args, **kwargs)
        return future

    def wait_for_all_tasks(self):
        """等待所有任务完成"""
        if self.executor is None:
            print("线程池未启动或已关闭")
            return
        for future in as_completed(self.executor.futures()):
            print(future.result())
