"""Export only RUA's aggregate GA4 page views; never publish credentials or raw reports."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

PUBLIC_URL = 'https://kairunwen.github.io/Awesome-Robot-Use-Agent/views.json'
START_DATE = '2026-09-13'


def snapshot(report):
    if [h['name'] for h in report.get('metricHeaders', [])] != ['screenPageViews']:
        raise ValueError('Unexpected GA4 metric')
    rows = report.get('rows', [])
    if len(rows) > 1:
        raise ValueError('Expected one aggregate row')
    value = rows[0]['metricValues'][0]['value'] if rows else '0'
    if not isinstance(value, str) or not value.isascii() or not value.isdecimal():
        raise ValueError('Invalid page-view total')
    return validate({'source': 'ga4', 'total': int(value), 'start_date': START_DATE,
                     'updated_at': datetime.now(timezone.utc).isoformat()})


def validate(data):
    if (data.get('source') != 'ga4' or data.get('start_date') != START_DATE
            or type(data.get('total')) is not int or not 0 <= data['total'] <= 2**53 - 1
            or datetime.fromisoformat(data['updated_at']).tzinfo is None):
        raise ValueError('Invalid views snapshot')
    return {key: data[key] for key in ('source', 'total', 'start_date', 'updated_at')}


def fetch_report():
    from google.oauth2.service_account import Credentials
    from google.auth.transport.requests import AuthorizedSession

    info = json.loads(os.environ['GA_SERVICE_ACCOUNT_JSON'])
    if info.get('type') != 'service_account':
        raise ValueError('Expected dedicated service account')
    info['token_uri'] = 'https://oauth2.googleapis.com/token'
    credentials = Credentials.from_service_account_info(
        info, scopes=['https://www.googleapis.com/auth/analytics.readonly'])
    with AuthorizedSession(credentials) as session:
        response = session.post(
            'https://analyticsdata.googleapis.com/v1beta/properties/553953217:runReport',
            json={'dateRanges': [{'startDate': START_DATE, 'endDate': 'today'}],
                  'metrics': [{'name': 'screenPageViews'}],
                  'dimensionFilter': {'filter': {'fieldName': 'streamId',
                      'stringFilter': {'matchType': 'EXACT', 'value': '15768875279'}}}},
            timeout=30)
        response.raise_for_status()
        return snapshot(response.json())


def previous_snapshot():
    with urlopen(PUBLIC_URL, timeout=15) as response:
        return validate(json.load(response))


def update(output):
    try:
        data = fetch_report()
    except Exception as error:
        # Preserve the timestamp too: failed refreshes must not look like fresh data.
        print(f'::warning::GA4 refresh failed ({type(error).__name__}); retaining published count.')
        data = previous_snapshot()  # If no valid previous count exists, stop deployment.
    output.write_text(json.dumps(data, indent=2) + '\n')
    print(f'Published GA4 snapshot: {data["total"]} page views, updated {data["updated_at"]}')


if __name__ == '__main__':
    try:
        update(Path(__file__).parent / 'dist' / 'views.json')
    except Exception as error:
        raise SystemExit(f'Views unavailable ({type(error).__name__}); deployment stopped.') from None
