
def framework(status="open", slug="g-cloud-7", name=None, clarification_questions_open=True, lots=None):
    if slug == "g-cloud-7":
        name = "G-Cloud 7"
    elif slug == "digital-outcomes-and-specialists":
        name = "Digital Outcomes and Specialists"
    else:
        name = slug.replace("-", " ").title()

    lots = lots or []

    return {
        "frameworks": {
            "id": 1,
            "status": status,
            "clarificationQuestionsOpen": clarification_questions_open,
            "name": name,
            "slug": slug,
            "lots": lots,
        }
    }


def lot(slug="some-lot", allows_brief=False, one_service_limit=False):
    return {
        "id": 1,
        "slug": slug,
        "name": slug.replace("-", " ").title(),
        "allowsBrief": allows_brief,
        "oneServiceLimit": one_service_limit,
    }


def brief(status="draft",
          framework_slug="digital-outcomes-and-specialists",
          lot_slug="digital-specialists",
          user_id=123,
          framework_name="Digital Outcomes and Specialists",
          clarification_questions=None,
          dates=None,
          clarification_questions_closed=False):

    DATES_PUBLISHED = {
      "answers_close": "2016-10-19T07:00:00+00:00",
      "application_open_weeks": "2 weeks",
      "closing_date": "2016-10-20",
      "closing_time": "2016-10-20T07:00:00+00:00",
      "published_date": "2016-10-06",
      "questions_close": "2016-10-13T07:00:00+00:00"
    }

    DATES_UNPUBLISHED = {
      "answers_close": None,
      "application_open_weeks": "2 weeks",
      "closing_date": None,
      "closing_time": None,
      "hypothetical": DATES_PUBLISHED,
      "published_date": None,
      "questions_close": None
    }

    brief = {
        "briefs": {
            "id": 1234,
            "title": "I need a thing to do a thing",
            "frameworkSlug": framework_slug,
            "frameworkName": framework_name,
            "lotSlug": lot_slug,
            "status": status,
            "users": [{"active": True,
                       "role": "buyer",
                       "emailAddress": "buyer@email.com",
                       "id": user_id,
                       "name": "Buyer User"}],
            "createdAt": "2016-03-29T10:11:12.000000+00:00",
            "updatedAt": "2016-03-29T10:11:13.000000+00:00",
            "clarificationQuestions": clarification_questions or [],
            "sellerSelector": 'allSellers'
        }
    }

    if status == "live":
        brief['briefs']['publishedAt'] = "2016-03-29T10:11:14.000000+00:00"
        brief['briefs']['dates'] = DATES_PUBLISHED
        brief['briefs']['applicationsClosedAt'] = "2016-04-07T00:00:00.000000+00:00"
        brief['briefs']['clarificationQuestionsClosedAt'] = "2016-04-02T00:00:00.000000+00:00"
        brief['briefs']['clarificationQuestionsAreClosed'] = clarification_questions_closed
        brief['briefs']['clarificationQuestionsPublishedBy'] = "2016-04-06T00:00:00.000000+00:00"
    else:
        brief['briefs']['dates'] = DATES_UNPUBLISHED

    return brief
