import re
import sys

from testrail.api import API
from testrail.case import Case
from testrail.configuration import Config, ConfigContainer
from testrail.helper import methdispatch, singleresult, TestRailError
from testrail.milestone import Milestone
from testrail.plan import Plan, PlanContainer
from testrail.entry import Entry
from testrail.project import Project, ProjectContainer
from testrail.result import Result, ResultContainer
from testrail.run import Run, RunContainer
from testrail.status import Status
from testrail.suite import Suite
from testrail.section import Section
from testrail.test import Test
from testrail.user import User
from testrail.priority import Priority
from testrail.casetype import CaseType
from testrail.template import Template

# pylint: disable=redefined-builtin
# pylint: disable=invalid-name
if sys.version_info >= (3, 0):
    unicode = str


# pylint: disable=no-self-use
# pylint: disable=too-many-public-methods
class TestRail(object):
    def __init__(self, project_id=0, email=None, key=None, url=None):
        self.api = API(email=email, key=key, url=url)
        self.api.set_project_id(project_id)
        self._project_id = project_id

    def set_project_id(self, project_id):
        self._project_id = project_id
        self.api.set_project_id(project_id)

    # Post generics
    @methdispatch
    def add(self, obj):
        raise NotImplementedError

    @methdispatch
    def update(self, obj):
        raise NotImplementedError

    @methdispatch
    def close(self, obj):
        raise NotImplementedError

    @methdispatch
    def delete(self, obj):
        raise NotImplementedError

    # Project Methods
    def projects(self):
        return ProjectContainer(list(map(Project, self.api.projects())))

    @methdispatch
    def project(self):
        return Project()

    @project.register(str)
    @project.register(unicode)
    @singleresult
    def _project_by_name(self, name):
        return filter(lambda p: p.name == name, self.projects())

    @project.register(int)
    @singleresult
    def _project_by_id(self, project_id):
        return filter(lambda p: p.id == project_id, self.projects())

    # User Methods
    def users(self):
        return map(User, self.api.users())

    @methdispatch
    def user(self):
        return User()

    @user.register(int)
    @singleresult
    def _user_by_id(self, identifier):
        return filter(lambda u: u.id == identifier, self.users())

    @user.register(str)
    @user.register(unicode)
    @singleresult
    def _user_by_email_name(self, identifier):
        by_email = lambda u: u.email == identifier
        by_name = lambda u: u.name == identifier
        f = by_email if re.match(r'[^@]+@[^@]+\.[^@]+', identifier) else by_name
        return filter(f, self.users())

    def active_users(self):
        return list(filter(lambda u: u.is_active is True, self.users()))

    def inactive_users(self):
        return list(filter(lambda u: u.is_active is False, self.users()))

    # Suite Methods
    def suites(self):
        return map(Suite, self.api.suites(self._project_id))

    @methdispatch
    def suite(self):
        return Suite()

    @suite.register(str)
    @suite.register(unicode)
    @singleresult
    def _suite_by_name(self, name):
        return filter(lambda s: s.name.lower() == name.lower(), self.suites())

    @suite.register(int)
    @singleresult
    def _suite_by_id(self, suite_id):
        return filter(lambda s: s.id == suite_id, self.suites())

    def active_suites(self):
        return filter(lambda s: s.is_completed is False, self.suites())

    def completed_suites(self):
        return filter(lambda s: s.is_completed is True, self.suites())

    @add.register(Suite)
    def add_suite(self, obj):
        obj.project = obj.project or self.project()
        return Suite(self.api.add_suite(obj.raw_data()))

    @update.register(Suite)
    def _update_suite(self, obj):
        return Suite(self.api.update_suite(obj.raw_data()))

    @delete.register(Suite)
    def _delete_suite(self, obj):
        return self.api.delete_suite(obj.id)

    # Milestone Methods
    def milestones(self):
        return map(Milestone, self.api.milestones(self._project_id))

    @methdispatch
    def milestone(self):
        return Milestone()

    @milestone.register(str)
    @milestone.register(unicode)
    @singleresult
    def _milestone_by_name(self, name):
        return filter(
            lambda m: m.name.lower() == name.lower(), self.milestones())

    @milestone.register(int)
    @singleresult
    def _milestone_by_id(self, milestone_id):
        return filter(lambda s: s.id == milestone_id, self.milestones())

    @add.register(Milestone)
    def _add_milestone(self, obj):
        obj.project = obj.project or self.project()
        return Milestone(self.api.add_milestone(obj.raw_data()))

    @update.register(Milestone)
    def _update_milestone(self, obj):
        return Milestone(self.api.update_milestone(obj.raw_data()))

    @delete.register(Milestone)
    def _delete_milestone(self, obj):
        return self.api.delete_milestone(obj.id)

    # Plan Methods
    @methdispatch
    def plans(self):
        return PlanContainer(list(map(Plan, self.api.plans(self._project_id))))

    @plans.register(Milestone)
    def _plans_for_milestone(self, obj):
        plans = filter(lambda p: p.milestone is not None, self.plans())
        return PlanContainer(filter(lambda p: p.milestone.id == obj.id, plans))

    @methdispatch
    def plan(self):
        return Plan()

    @plan.register(str)
    @plan.register(unicode)
    @singleresult
    def _plan_by_name(self, name):
        return filter(lambda p: p.name.lower() == name.lower(), self.plans())

    @plan.register(int)
    @singleresult
    def _plan_by_id(self, plan_id):
        return filter(lambda p: p.id == plan_id, self.plans())

    def completed_plans(self):
        return filter(lambda p: p.is_completed is True, self.plans())

    def active_plans(self):
        return filter(lambda p: p.is_completed is False, self.plans())

    @add.register(Plan)
    def _add_plan(self, obj, milestone=None):
        obj.project = obj.project or self.project()
        obj.milestone = milestone or obj.milestone
        return Plan(self.api.add_plan(obj.raw_data()))

    @update.register(Plan)
    def _update_plan(self, obj):
        return Plan(self.api.update_plan(obj.raw_data()))

    @close.register(Plan)
    def _close_plan(self, obj):
        return Plan(self.api.close_plan(obj.id))

    @delete.register(Plan)
    def _delete_plan(self, obj):
        return self.api.delete_plan(obj.id)

    # Plan Entries Methods

    @methdispatch
    def plan_entry(self):
        # pylint: disable=no-value-for-parameter
        return Entry()

    @add.register(Entry)
    def add_plan_entry(self, obj, plan_id):
        return Entry(self.api.add_plan_entry(obj.raw_data(), plan_id))

    # Run Methods
    @methdispatch
    def runs(self):
        return RunContainer(list(map(Run, self.api.runs(self._project_id))))

    @runs.register(Milestone)
    def _runs_for_milestone(self, obj):
        return RunContainer(filter(
            lambda r: r.milestone.id == obj.id, self.runs()))

    @runs.register(str)
    @runs.register(unicode)
    def _runs_by_name(self, name):
        # Returns all Runs that match :name, in descending order by ID
        runs = list(filter(lambda r: r.name.lower() == name.lower(), self.runs()))
        return sorted(runs, key=lambda r: r.id)

    @methdispatch
    def run(self):
        return Run()

    @run.register(str)
    @run.register(unicode)
    @singleresult
    def _run_by_name(self, name):
        # Returns the most recently created Run that matches :name
        runs = list(filter(lambda r: r.name.lower() == name.lower(), self.runs()))
        return sorted(runs, key=lambda r: r.id)[:1]

    @run.register(int)
    @singleresult
    def _run_by_id(self, run_id):
        return filter(lambda p: p.id == run_id, self.runs())

    @run.register(int)
    @singleresult
    def _run_by_project_suite(self, project, suite):
        return filter(lambda p: p.project_id == project.id and p.suite.id == suite.id, self.runs())

    @add.register(Run)
    def _add_run(self, obj):
        obj.project = obj.project or self.project()
        return Run(self.api.add_run(obj.raw_data()))

    @update.register(Run)
    def _update_run(self, obj):
        return Run(self.api.update_run(obj.raw_data()))

    @close.register(Run)
    def _close_run(self, obj):
        return Run(self.api.close_run(obj.id))

    @delete.register(Run)
    def _delete_run(self, obj):
        return self.api.delete_run(obj.id)

    # Case Methods
    def cases(self, suite):
        return map(Case, self.api.cases(self._project_id, suite.id))

    @methdispatch
    def case(self):
        return Case()

    @case.register(str)
    @case.register(unicode)
    @singleresult
    def _case_by_title(self, title, suite):
        return filter(
            lambda c: c.title.lower() == title.lower(), self.cases(suite))

    @case.register(int)
    @singleresult
    def _case_by_id(self, case_id, suite=None):
        return filter(lambda c: c.id == case_id, self.cases(suite))

    @add.register(Case)
    def add_case(self, obj):
        return Case(self.api.add_case(obj.raw_data()))

    @update.register(Case)
    def update_case(self, obj):
        return Case(self.api.update_case(obj.raw_data()))

    # Test Methods
    def tests(self, run):
        return map(Test, self.api.tests(run.id))

    @methdispatch
    def test(self):
        return Test()

    @test.register(str)
    @test.register(unicode)
    @singleresult
    def _test_by_name(self, name, run):
        return filter(lambda t: t.name.lower() == name.lower(), self.tests(run))

    @test.register(int)
    @singleresult
    def _test_by_id(self, test_id, run):
        return filter(
            lambda t: t.raw_data()['case_id'] == test_id, self.tests(run))

    # Result Methods
    @methdispatch
    def results(self):
        raise TestRailError("Must request results by Run or Test")

    @results.register(Run)
    def _results_for_run(self, run):
        return ResultContainer(list(map(Result, self.api.results_by_run(run.id))))

    @results.register(Test)
    def _results_for_test(self, test):
        return ResultContainer(list(map(Result, self.api.results_by_test(test.id))))

    @methdispatch
    def result(self):
        return Result()

    @add.register(Result)
    def _add_result(self, obj):
        self.api.add_result(obj.raw_data())

    @add.register(tuple)
    def add_results(self, results):
        obj, value = results
        if isinstance(obj, Run):
            self.api.add_results(map(lambda x: x.raw_data(), value), obj.id)

    @add.register(tuple)
    def _add_results_for_cases(self, obj, run_id):
        self.api.add_results_for_cases(obj, run_id)

    # Section Methods
    def sections(self, suite=None):
        return map(Section, self.api.sections(suite_id=suite.id))

    @methdispatch
    def section(self):
        return Section()

    @section.register(int)
    def _section_by_id(self, section_id):
        return Section(self.api.section_with_id(section_id))

    @section.register(unicode)
    @section.register(str)
    @singleresult
    def _section_by_name(self, name, suite=None):
        return filter(lambda s: s.name == name, self.sections(suite))

    @add.register(Section)
    def add_section(self, section):
        return Section(self.api.add_section(section.raw_data()))

    # Status Methods
    def statuses(self):
        return map(Status, self.api.statuses())

    @methdispatch
    def status(self):
        # pylint: disable=no-value-for-parameter
        return Status()

    @status.register(str)
    @status.register(unicode)
    @singleresult
    def _status_by_name(self, name):
        return filter(lambda s: s.name == name.lower(), self.statuses())

    @status.register(int)
    @singleresult
    def _status_by_id(self, status_id):
        return filter(lambda s: s.id == status_id, self.statuses())

    # Priority Methods
    def priorities(self):
        return map(Priority, self.api.priorities())

    @methdispatch
    def priority(self):
        # pylint: disable=no-value-for-parameter
        return Priority()

    @priority.register(str)
    @priority.register(unicode)
    @singleresult
    def _priority_by_name(self, name):
        return filter(lambda s: s.name == name.lower(), self.priorities())

    @priority.register(int)
    @singleresult
    def _priority_by_id(self, priority_id):
        return filter(lambda s: s.id == priority_id, self.priorities())

    # Template Methods
    def templates(self):
        return map(Template, self.api.templates())

    @methdispatch
    def template(self):
        # pylint: disable=no-value-for-parameter
        return Template()

    @template.register(str)
    @template.register(unicode)
    @singleresult
    def _template_by_name(self, name):
        return filter(lambda s: s.name == name.lower(), self.templates())

    @template.register(int)
    @singleresult
    def _template_by_id(self, template_id):
        return filter(lambda s: s.id == template_id, self.templates())

    # CaseType Methods
    def case_types(self):
        return map(CaseType, self.api.case_types())

    @methdispatch
    def case_type(self):
        # pylint: disable=no-value-for-parameter
        return CaseType()

    @case_type.register(str)
    @case_type.register(unicode)
    @singleresult
    def _case_type_by_name(self, name):
        return filter(lambda s: s.name == name.lower(), self.case_types())

    @case_type.register(int)
    @singleresult
    def _case_type_by_id(self, case_type_id):
        return filter(lambda s: s.id == case_type_id, self.case_types())

    def configs(self):
        return ConfigContainer(map(Config, self.api.configs()))
