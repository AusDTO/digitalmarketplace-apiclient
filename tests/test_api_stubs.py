from dmapiclient import api_stubs


def test_framework():
    assert api_stubs.framework() == {
        "frameworks": {
            "clarificationQuestionsOpen": True,
            "lots": [],
            "name": "G-Cloud 7",
            "slug": "g-cloud-7",
            "status": "open",
        }
    }


def test_framework_name_changes_with_slug():
    assert api_stubs.framework(slug='digital-outcomes-and-specialists')["frameworks"]["name"] == \
        "Digital Outcomes and Specialists"
    assert api_stubs.framework(slug="my-framework")["frameworks"]["name"] == "My Framework"


def test_lot_name_default_is_made_from_slug():
    assert api_stubs.lot(slug="my-lot")["name"] == "My Lot"


def test_lot():
    assert api_stubs.lot(slug="foo") == {
        "id": 1,
        "slug": "foo",
        "name": "Foo",
        "allowsBrief": False,
        "oneServiceLimit": False,
    }


def test_brief():
    assert api_stubs.brief() \
        == {
        "briefs": {
            "id": 1234,
            "title": "I need a thing to do a thing",
            "frameworkSlug": "digital-outcomes-and-specialists",
            "frameworkName": "Digital Outcomes and Specialists",
            "lotSlug": "digital-specialists",
            "status": "draft",
            "users": [{"active": True,
                       "role": "buyer",
                       "emailAddress": "buyer@email.com",
                       "id": 123,
                       "name": "Buyer User"}],
            "createdAt": "2016-03-29T10:11:12.000000+00:00",
            "updatedAt": "2016-03-29T10:11:13.000000+00:00",
            "clarificationQuestions": [],
            "sellerSelector": 'allSellers',
            "dates": {
                "answers_close": None,
                "application_open_weeks": "2 weeks",
                "closing_date": None,
                "closing_time": None,
                "hypothetical": {
                    "answers_close": "2016-10-19T07:00:00+00:00",
                    "application_open_weeks": "2 weeks",
                    "closing_date": "2016-10-20",
                    "closing_time": "2016-10-20T07:00:00+00:00",
                    "published_date": "2016-10-06",
                    "questions_close": "2016-10-13T07:00:00+00:00"
                },
                "published_date": None,
                "questions_close": None
            }
        }
    }

    assert api_stubs.brief(
        status='live',
        framework_slug='a-framework-slug',
        lot_slug='a-lot-slug', user_id=234,
        framework_name='A Framework Name') \
        == {
        "briefs": {
            "id": 1234,
            "title": "I need a thing to do a thing",
            "frameworkSlug": "a-framework-slug",
            "frameworkName": "A Framework Name",
            "lotSlug": "a-lot-slug",
            "status": "live",
            "users": [{"active": True,
                       "role": "buyer",
                       "emailAddress": "buyer@email.com",
                       "id": 234,
                       "name": "Buyer User"}],
            "createdAt": "2016-03-29T10:11:12.000000+00:00",
            "updatedAt": "2016-03-29T10:11:13.000000+00:00",
            "publishedAt": "2016-03-29T10:11:14.000000+00:00",
            "applicationsClosedAt": "2016-04-07T00:00:00.000000+00:00",
            "clarificationQuestionsClosedAt": "2016-04-02T00:00:00.000000+00:00",
            "clarificationQuestionsPublishedBy": "2016-04-06T00:00:00.000000+00:00",
            "clarificationQuestionsAreClosed": False,
            "clarificationQuestions": [],
            "sellerSelector": 'allSellers',
            "dates": {
              "answers_close": "2016-10-19T07:00:00+00:00",
              "application_open_weeks": "2 weeks",
              "closing_date": "2016-10-20",
              "closing_time": "2016-10-20T07:00:00+00:00",
              "published_date": "2016-10-06",
              "questions_close": "2016-10-13T07:00:00+00:00"
            }
        }
    }

    assert api_stubs.brief(clarification_questions=[{"question": "Why?", "answer": "Because"}]) \
        == {
        "briefs": {
            "id": 1234,
            "title": "I need a thing to do a thing",
            "frameworkSlug": "digital-outcomes-and-specialists",
            "frameworkName": "Digital Outcomes and Specialists",
            "lotSlug": "digital-specialists",
            "status": "draft",
            "users": [{"active": True,
                       "role": "buyer",
                       "emailAddress": "buyer@email.com",
                       "id": 123,
                       "name": "Buyer User"}],
            "createdAt": "2016-03-29T10:11:12.000000+00:00",
            "updatedAt": "2016-03-29T10:11:13.000000+00:00",
            "clarificationQuestions": [{
                "question": "Why?",
                "answer": "Because"
            }],
            "sellerSelector": 'allSellers',
            "dates": {
                "answers_close": None,
                "application_open_weeks": "2 weeks",
                "closing_date": None,
                "closing_time": None,
                "published_date": None,
                "questions_close": None,
                "hypothetical": {
                    "answers_close": "2016-10-19T07:00:00+00:00",
                    "application_open_weeks": "2 weeks",
                    "closing_date": "2016-10-20",
                    "closing_time": "2016-10-20T07:00:00+00:00",
                    "published_date": "2016-10-06",
                    "questions_close": "2016-10-13T07:00:00+00:00"
                }
            }
        }
    }

    assert api_stubs.brief(status='live', clarification_questions_closed=True) \
        == {
        "briefs": {
            "id": 1234,
            "title": "I need a thing to do a thing",
            "frameworkSlug": "digital-outcomes-and-specialists",
            "frameworkName": "Digital Outcomes and Specialists",
            "lotSlug": "digital-specialists",
            "status": "live",
            "users": [{"active": True,
                       "role": "buyer",
                       "emailAddress": "buyer@email.com",
                       "id": 123,
                       "name": "Buyer User"}],
            "createdAt": "2016-03-29T10:11:12.000000+00:00",
            "updatedAt": "2016-03-29T10:11:13.000000+00:00",
            "publishedAt": "2016-03-29T10:11:14.000000+00:00",
            "applicationsClosedAt": "2016-04-07T00:00:00.000000+00:00",
            "clarificationQuestionsClosedAt": "2016-04-02T00:00:00.000000+00:00",
            "clarificationQuestionsPublishedBy": "2016-04-06T00:00:00.000000+00:00",
            "clarificationQuestionsAreClosed": True,
            "clarificationQuestions": [],
            "sellerSelector": 'allSellers',
            "dates": {
              "answers_close": "2016-10-19T07:00:00+00:00",
              "application_open_weeks": "2 weeks",
              "closing_date": "2016-10-20",
              "closing_time": "2016-10-20T07:00:00+00:00",
              "published_date": "2016-10-06",
              "questions_close": "2016-10-13T07:00:00+00:00"
            }
        }
    }
