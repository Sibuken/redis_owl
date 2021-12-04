from case_1.redis_streams import (
    test_invalidation_redis_stream,
    test_push_new_article_redis_stream,
    test_pagination_redis_stream,
    test_pagination_after_add_article_redis_stream,
)
from case_1.redis_list import (
    test_pagination_redis_list,
    test_pagination_after_add_article_redis_list,
    test_simple_read_redis_list,
)
from case_2.redis_hash import (
    test_get_all_speakers_from_cache,
    test_get_speakers_by_language,
)


if __name__ == "__main__":
    test_invalidation_redis_stream()
    test_push_new_article_redis_stream()
    test_pagination_redis_stream()
    test_pagination_after_add_article_redis_stream()
    test_pagination_redis_list()
    test_pagination_after_add_article_redis_list()
    test_simple_read_redis_list()
    test_get_all_speakers_from_cache()
    test_get_speakers_by_language()
