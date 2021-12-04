def test_pagination_after_add_article_redis_list():
    init_environment()
    response = link_read_articles_from_list()
    start = response["start"]

    response_2 = link_read_articles_from_list(start=start)

    link_add_article_to_redis_list()

    response_3 = link_read_articles_from_list(start=start)
