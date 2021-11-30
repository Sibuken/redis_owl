from case_1.redis_streams import (
    test_invalidation_redis_stream,
    test_push_new_article_redis_stream,
    test_pagination_redis_stream,
    test_pagination_after_add_article_redis_stream,
)


if __name__ == "__main__":
    test_invalidation_redis_stream()
    test_push_new_article_redis_stream()
    test_pagination_redis_stream()
    test_pagination_after_add_article_redis_stream()
