## 背景
> 由于原生的apscheduler仅支持redis单节点连接，不支持redis集群，所以本人基于原生的`RedisJobStore`自己修改了一个专门用于连接redis集群的类`RedisClusterJobStore`
修改点有以下内容：
> 1. 修改类名`RedisJobStore`为`RedisClusterJobStore`
> 2. 将原始导入的`redis`替换为`rediscluster`
> 3. 将原始代码中的`pipe.multi()`注释掉，此处注释掉是否会有其他的影响暂未测试

## 文件
```
# encoding:utf8
from __future__ import absolute_import
from datetime import datetime

from pytz import utc
import six

from apscheduler.jobstores.base import BaseJobStore, JobLookupError, ConflictingIdError
from apscheduler.util import datetime_to_utc_timestamp, utc_timestamp_to_datetime
from apscheduler.job import Job

try:
    import cPickle as pickle
except ImportError:  # pragma: nocover
    import pickle

try:
    # from redis import Redis
    from rediscluster import RedisCluster # 将原本的redis库替换为rediscluster
except ImportError:  # pragma: nocover
    raise ImportError('RedisJobStore requires redis installed')


class RedisClusterJobStore(BaseJobStore):
    """
    Stores jobs in a Redis database. Any leftover keyword arguments are directly passed to redis's
    :class:`~redis.StrictRedis`.

    Plugin alias: ``redis``

    :param int db: the database number to store jobs in
    :param str jobs_key: key to store jobs in
    :param str run_times_key: key to store the jobs' run times in
    :param int pickle_protocol: pickle protocol level to use (for serialization), defaults to the
        highest available
    """

    def __init__(self, db=0, jobs_key='apscheduler.jobs', run_times_key='apscheduler.run_times',
                 pickle_protocol=pickle.HIGHEST_PROTOCOL, **connect_args):
        super(RedisClusterJobStore, self).__init__()

        if db is None:
            raise ValueError('The "db" parameter must not be empty')
        if not jobs_key:
            raise ValueError('The "jobs_key" parameter must not be empty')
        if not run_times_key:
            raise ValueError('The "run_times_key" parameter must not be empty')

        self.pickle_protocol = pickle_protocol
        self.jobs_key = jobs_key
        self.run_times_key = run_times_key
        # self.redis = Redis(db=int(db), **connect_args)
        self.redis = RedisCluster(**connect_args)

    def lookup_job(self, job_id):
        job_state = self.redis.hget(self.jobs_key, job_id)
        return self._reconstitute_job(job_state) if job_state else None

    def get_due_jobs(self, now):
        timestamp = datetime_to_utc_timestamp(now)
        job_ids = self.redis.zrangebyscore(self.run_times_key, 0, timestamp)
        if job_ids:
            job_states = self.redis.hmget(self.jobs_key, *job_ids)
            return self._reconstitute_jobs(six.moves.zip(job_ids, job_states))
        return []

    def get_next_run_time(self):
        next_run_time = self.redis.zrange(self.run_times_key, 0, 0, withscores=True)
        if next_run_time:
            return utc_timestamp_to_datetime(next_run_time[0][1])

    def get_all_jobs(self):
        job_states = self.redis.hgetall(self.jobs_key)
        jobs = self._reconstitute_jobs(six.iteritems(job_states))
        paused_sort_key = datetime(9999, 12, 31, tzinfo=utc)
        return sorted(jobs, key=lambda job: job.next_run_time or paused_sort_key)

    def add_job(self, job):
        if self.redis.hexists(self.jobs_key, job.id):
            raise ConflictingIdError(job.id)

        with self.redis.pipeline() as pipe:
            # pipe.multi()
            pipe.hset(self.jobs_key, job.id, pickle.dumps(job.__getstate__(),
                                                          self.pickle_protocol))
            if job.next_run_time:
                pipe.zadd(self.run_times_key,
                          {job.id: datetime_to_utc_timestamp(job.next_run_time)})

            pipe.execute()

    def update_job(self, job):
        if not self.redis.hexists(self.jobs_key, job.id):
            raise JobLookupError(job.id)

        with self.redis.pipeline() as pipe:
            pipe.hset(self.jobs_key, job.id, pickle.dumps(job.__getstate__(),
                                                          self.pickle_protocol))
            if job.next_run_time:
                pipe.zadd(self.run_times_key,
                          {job.id: datetime_to_utc_timestamp(job.next_run_time)})
            else:
                pipe.zrem(self.run_times_key, job.id)

            pipe.execute()

    def remove_job(self, job_id):
        if not self.redis.hexists(self.jobs_key, job_id):
            raise JobLookupError(job_id)

        with self.redis.pipeline() as pipe:
            pipe.hdel(self.jobs_key, job_id)
            pipe.zrem(self.run_times_key, job_id)
            pipe.execute()

    def remove_all_jobs(self):
        with self.redis.pipeline() as pipe:
            pipe.delete(self.jobs_key)
            pipe.delete(self.run_times_key)
            pipe.execute()

    def shutdown(self):
        self.redis.connection_pool.disconnect()

    def _reconstitute_job(self, job_state):
        job_state = pickle.loads(job_state)
        job = Job.__new__(Job)
        job.__setstate__(job_state)
        job._scheduler = self._scheduler
        job._jobstore_alias = self._alias
        return job

    def _reconstitute_jobs(self, job_states):
        jobs = []
        failed_job_ids = []
        for job_id, job_state in job_states:
            try:
                jobs.append(self._reconstitute_job(job_state))
            except BaseException:
                self._logger.exception('Unable to restore job "%s" -- removing it', job_id)
                failed_job_ids.append(job_id)

        # Remove all the jobs we failed to restore
        if failed_job_ids:
            with self.redis.pipeline() as pipe:
                pipe.hdel(self.jobs_key, *failed_job_ids)
                pipe.zrem(self.run_times_key, *failed_job_ids)
                pipe.execute()

        return jobs

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
```
## 如何使用
```
from aaa import RedisClusterJobStore

# 配置 Redis集群 作为 JobStore
jobstore = {
    'default': RedisClusterJobStore(startup_nodes=[{"host": "127.0.0.1", "port": 7000}],passoword="test1234")
}
executors={
	'default': ThreadPoolExecutor()
}

scheduler = BackgroundScheduler(jobstores=jobstore, executors=executors)
# 定义一个任务
def job_function():
    print("Hello World!")

# 添加任务到调度器
scheduler.add_job(job_function, 'interval', seconds=5)
scheduler.start()

```
