from statistics import median
from datetime import datetime
import analytical.func_api_client as fa
from req_response import resp_json


class BugIssuesAnalytic:
    def __init__(self):
        self.bug_issues_closed_total_count = 0
        self.bug_issues_open_total_count = 0
        self.bug_issues_no_comment = 0
        self.bug_issues_duration_closed_list = []
        self.bug_issues_duration_open_list = []

    async def push_bug_issues(self, data):
        now_time = datetime.utcnow()
        for bug_issue in data:
            created_at = await fa.to_date(bug_issue["node"]["createdAt"])
            comment_count = bug_issue["node"]["comments"]["totalCount"]
            if bug_issue["node"]["comments"]["nodes"]:
                last_comment = bug_issue["node"]["comments"]["nodes"][0]["createdAt"]
            else:
                last_comment = None

            if bug_issue["node"]["closed"]:
                closed_at = await fa.to_date(bug_issue["node"]["closedAt"])
                self.bug_issues_closed_total_count += 1
                self.bug_issues_duration_closed_list.append(closed_at - created_at)
            else:
                self.bug_issues_open_total_count += 1
                self.bug_issues_duration_open_list.append(now_time - created_at)
            if not comment_count:
                self.bug_issues_no_comment += 1

    async def get_bug_analytic(self):
        closed_list_len = len(self.bug_issues_duration_closed_list)
        open_list_len = len(self.bug_issues_duration_open_list)
        bug_issues_closed_two_months = None
        if closed_list_len >= 10:
            bug_issues_closed_two_months = 0
            self.bug_issues_duration_closed_list.sort()
            resp_json.analytic.closed_bug_95perc = self.bug_issues_duration_closed_list[
                round((closed_list_len - 1) * 0.95)
            ].days
            resp_json.analytic.closed_bug_50perc = median(
                self.bug_issues_duration_closed_list
            ).days
            for i in range(closed_list_len):
                if self.bug_issues_duration_closed_list[i].days < 60:
                    bug_issues_closed_two_months += 1
                else:
                    break
        resp_json.repository_info.bug_issues_closed_count = (
            self.bug_issues_closed_total_count
        )
        resp_json.repository_info.bug_issues_open_count = (
            self.bug_issues_open_total_count
        )
        if resp_json.repository_info.bug_issues_count:
            resp_json.analytic.bug_issues_no_comment = round(
                self.bug_issues_no_comment
                / resp_json.repository_info.bug_issues_count
                * 100,
                2,
            )
        if (
            resp_json.repository_info.bug_issues_closed_count
            and bug_issues_closed_two_months
        ):
            resp_json.analytic.bug_issues_closed_2months = round(
                bug_issues_closed_two_months
                / resp_json.repository_info.bug_issues_closed_count
                * 100,
                2,
            )
