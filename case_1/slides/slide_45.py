def test_pagination_after_add_article_redis_stream():
    init_environment()
    response = read_ordered_data_from_stream()
    start_id = response["start_id"]
    response_2 = read_ordered_data_from_stream(start_id=start_id)

    add_article_to_redis_stream()

    response_3 = read_ordered_data_from_stream(start_id=start_id)
