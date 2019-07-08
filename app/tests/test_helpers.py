
def assert_mood_in_response(test_case, mood, data):
    test_case.assertTrue(any(
        item['id'] == mood.public_id for item in data))
    test_case.assertTrue(any(
        item['name'] == mood.name for item in data))
    test_case.assertTrue(any(
        item['colour'] == mood.colour for item in data))
    test_case.assertTrue(any(
        item['template_id'] == mood.template.public_id for item in data))
