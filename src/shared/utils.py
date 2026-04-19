def redis_zmove(redis_instance, src_zset_name, dest_zset_name, value):
    val_score = redis_instance.zscore(src_zset_name, value)

    if val_score is not None:
        pl = redis_instance.pipeline()
        pl.zrem(src_zset_name, str(value))
        pl.zadd(dest_zset_name, {str(value): val_score})
        pl.execute()
        return True

    return False
