from __future__ import print_function

import json
from typing import List

from pytest_testrail.helper import TestRailError
from pytest_testrail.model.case import Case
from pytest_testrail.model.result import Result
from pytest_testrail.model.section import Section
from pytest_testrail.model.suite import Suite
from pytest_testrail.testrail_api import TestRailAPI

SEPARATOR_CHAR = ' - '


def export_tests(tr: TestRailAPI, project_id: int, project_name: str, feature):
    # Get a reference to the current project and dependencies
    tr_project = tr.projects.get_project(project_id=project_id)
    print('Collected project %s from TestRail' % tr_project.name)

    feature_name_raw = feature['feature']['name'].strip()
    feature_description = feature['feature']['description'].replace('\n  ', '\n').strip()
    tr_project_suite = get_project_suite(tr, tr_project.id, feature_name_raw.split(SEPARATOR_CHAR)[0])

    print('Collecting Cases for suite %s from TestRail' % tr_project_suite.name)
    tr_suite_cases = tr.cases.get_cases(project_id=tr_project.id, suite_id=tr_project_suite.id)

    raw_custom_preconds = []
    for scenario in feature['feature']['children']:
        if scenario['keyword'] == 'Background':
            print('Collecting Case preconditions')
            raw_custom_preconds = list('**' + rs['keyword'] + ':** ' + rs['text'] for rs in scenario['steps'])
            continue
        else:
            if any('component_test' in sc['name'] for sc in scenario['tags']):
                suite_section = {
                    'name': 'Default Test Cases',
                    'description': 'Default Section',
                    'display_order': 1
                }
            else:
                suite_section = {
                    'name': feature_name_raw.split(SEPARATOR_CHAR)[1],
                    'description': feature_description,
                    'display_order': 2
                }
            tr_suite_section = get_suite_section(tr, tr_project.id, tr_project_suite, suite_section)

        if 'examples' in scenario:
            examples_raw = scenario['examples'][0]

            table_rows = []
            table_header = examples_raw['tableHeader']['cells']
            for i in range(examples_raw['tableBody'].__len__()):
                table_row = examples_raw['tableBody'][i]
                row = {}
                for j in range(table_row['cells'].__len__()):
                    row.update({table_header[j]['value']: table_row['cells'][j]['value']})
                table_rows.append(row)

            for table_row in table_rows:
                raw_custom_data_set = json.dumps(table_row, indent=4, ensure_ascii=False)
                raw_case = build_case(tr=tr, project_id=tr_project.id, suite_id=tr_project_suite.id,
                                      section_id=tr_suite_section.id, feature=feature, scenario=scenario,
                                      raw_custom_preconds=raw_custom_preconds, raw_custom_data_set=raw_custom_data_set,
                                      project_name=project_name)
                export_case(tr, tr_suite_section.id, tr_suite_cases, raw_case)
        else:
            raw_case = build_case(tr=tr, project_id=tr_project.id, suite_id=tr_project_suite.id,
                                  section_id=tr_suite_section.id, feature=feature, scenario=scenario,
                                  raw_custom_preconds=raw_custom_preconds, raw_custom_data_set=None,
                                  project_name=project_name)
            export_case(tr, tr_suite_section.id, tr_suite_cases, raw_case)


def export_tests_results(tr: TestRailAPI, project_variables: dict, scenarios_run: list, env_name: str):
    print('\nPublishing results')
    tr_active_plans = tr.plans.get_plans(project_variables['id'], is_completed=0)
    tr_plan = next((plan for plan in tr_active_plans if plan.name == project_variables['test_plan']), None)
    if tr_plan is None:
        raise TestRailError('No Test Plan set with name %s for Automation Testing' % project_variables['test_plan'])
    tr_plan = tr.plans.get_plan(tr_plan.id)
    tr_statuses = tr.statuses.get_statuses()

    plan_entry_names = [plan_entry.name for plan_entry in tr_plan.entries]
    feature_names = scenarios_run.keys()

    if feature_names.__len__() > plan_entry_names.__len__() \
        or not set(feature_names).issubset(plan_entry_names):
        print('Not all test results will be published. Missing Test Suites: %s' % list(
            set(feature_names) - set(plan_entry_names)))

    for tr_plan_entry in tr_plan.entries:
        for tr_run in tr_plan_entry.runs:
            tr_results = []
            if tr_run.config == env_name and tr_run.name in scenarios_run:
                for scenario_run in scenarios_run[tr_run.name]:
                    tr_tests = tr.tests.get_tests(tr_run.id)
                    tr_test = next((test for test in tr_tests if test.title == scenario_run.name
                                    and (test.custom_methods['custom_data_set'] is None
                                         or ('custom_data_set' in test.custom_methods
                                             and json.loads(
                                test.custom_methods['custom_data_set']) == scenario_run.data_set)))
                                   , None)

                    if tr_test is None:
                        print('Result for test %s not published to TestRail' % scenario_run.name)
                    else:
                        custom_step_results = []
                        custom_steps_separated = tr_test.custom_methods['custom_steps_separated']
                        passed = True
                        for scenario_step, tr_case_step in zip(scenario_run.steps, custom_steps_separated):
                            status_type = 'blocked' if not passed \
                                else 'passed' if not scenario_step.failed \
                                else 'failed' if scenario_step.failed \
                                else 'untested'
                            if status_type == 'failed':
                                passed = False
                            status_id = next((st.id for st in tr_statuses if st.name == status_type), None)
                            exception_message = '' if status_type != 'failed' or not hasattr(scenarios_run,
                                                                                             'exception_message') else scenario_run.exception_message
                            custom_step_results.append({
                                'content': tr_case_step['content'],
                                'expected': tr_case_step['expected'],
                                'actual': exception_message,
                                'status_id': status_id
                            })
                        status_type = 'failed' if scenario_run.failed else 'passed'
                        tr_result = Result({
                            'test_id': tr_test.id,
                            'status_id': next(st.id for st in tr_statuses if st.name == status_type),
                            'comment': '',
                            'custom_step_results': custom_step_results
                        })
                        tr_results.append(tr_result)

            if tr_results.__len__() != 0:
                tr.results.add_results(tr_run.id, tr_results)
    print('\nResults published')


# pylint: disable=too-many-arguments
def build_case(tr: TestRailAPI, project_id: int, suite_id: int, section_id: int, feature, scenario, raw_custom_preconds,
               raw_custom_data_set=None, project_name=None) -> Case:
    # Setting Case references
    feature_refs = [ft for ft in feature['feature']['tags'] if project_name + '-' in ft['name']]
    scenario_refs = [sc for sc in scenario['tags'] if project_name + '-' in sc['name']]
    raw_refs = ', '.join(tg['name'].replace('@', '') for tg in (feature_refs + scenario_refs))

    # Setting Case tags
    raw_custom_tags = [sc['name'] for sc in scenario['tags']
                       if ('automated' not in sc['name']
                           and 'manual' not in sc['name'])] + \
                      [ft['name'] for ft in feature['feature']['tags']
                       if ('automated' not in ft['name']
                           and 'manual' not in ft['name']
                           and 'nondestructive' not in ft['name']
                           and project_name + '-' not in ft['name'])]

    # Setting Case priority
    priority_name = 'Critical' if filter(lambda sc: 'smoke' in sc['name'], scenario['tags']) \
        else 'High' if filter(lambda sc: 'sanity' in sc['name'], scenario['tags']) \
        else 'Medium' if filter(lambda sc: 'regression' in sc['name'], scenario['tags']) \
        else 'Low'
    raw_priority = next((pr.id for pr in tr.priorities.get_priorities() if pr.name == priority_name), None)

    # Setting Case type
    raw_type = next((ct.id for ct in tr.case_types.get_case_types() if ct.name == 'Functional'), None)

    # Setting Case template
    raw_template = next((ct.id for ct in tr.templates.get_templates(project_id) if ct.name == 'Test Case (Steps)'),
                        None)

    # Setting Case automation
    raw_custom_automation_type = '2' if any('stencil-automated' in sc['name'] for sc in scenario['tags']) \
        else '1' if any('automated' in sc['name'] for sc in scenario['tags']) else '0'

    # Setting Case steps
    raw_steps = [{'content': rs, 'expected': ''} for rs in raw_custom_preconds]
    raw_steps.extend([
        {
            'content': '**' + rs['keyword'].strip() + ':** ' + rs['text'].strip() + add_data_table(rs),
            'expected': ''
        }
        for rs in scenario['steps']])
    raw_case = Case({
        'estimate': '10m',
        'priority_id': raw_priority,
        'refs': raw_refs,
        'custom_tags': ', '.join(raw_custom_tags),
        'suite_id': suite_id,
        'section_id': section_id,
        'title': scenario['name'],
        'type_id': raw_type,
        'template_id': raw_template,
        'custom_automation_type': raw_custom_automation_type,
        'custom_data_set': raw_custom_data_set,
        'custom_preconds': '\n'.join(str(rp) for rp in raw_custom_preconds),
        'custom_steps_separated': raw_steps
    })
    return raw_case


def add_data_table(scenario_step):
    if 'argument' not in scenario_step:
        return ''
    data_table = '\n*Data Table*\n'
    table_rows = [rsa for rsa in scenario_step['argument']['rows']]
    for i, table_row in enumerate(table_rows):
        for j, rowCell in enumerate(table_row['cells']):
            data_table += ('|%s' % rowCell['value'])
        data_table += '|\n'
    return data_table


# pylint: disable=protected-access
def export_case(tr: TestRailAPI, section_id: int, tr_suite_cases: List[Case], raw_case: Case):
    tr_suite_case = next((sc for sc in tr_suite_cases
                          if sc.title == raw_case.title
                          and sc._custom_methods['custom_data_set'] == raw_case._custom_methods['custom_data_set'])
                         , None)
    if tr_suite_case:
        print('Upgrading Case ', tr_suite_case.title)
        tr.cases.update_case(case_id=tr_suite_case.id, case=raw_case)
    else:
        print('Creating Case ', raw_case.title)
        tr.cases.add_case(section_id=section_id, case=raw_case)


def get_project_test_plan(tr, tr_plan_name, test_market):
    test_plan_name = '%s_%s' % (tr_plan_name, test_market)
    tr_plans = tr.plans()
    tr_plan = next((tp for tp in tr_plans if tp.name == test_plan_name), None)
    if tr_plan is None:
        error_message = 'There is no Test Plan with name %s set on TestRail' % test_plan_name
        raise TestRailError(error_message)
    print('Collecting Test Plan ', tr_plan.name, ' from TestRail')
    return tr_plan


def get_project_suite(tr: TestRailAPI, tr_project_id: int, feature_name) -> Suite:
    tr_project_suites = tr.suites.get_suites(tr_project_id)
    if any((tr_project_suite.name == feature_name) for tr_project_suite in tr_project_suites):
        print('Collecting Suite ', feature_name, ' from TestRail')
        return next((ps for ps in tr_project_suites if ps.name == feature_name))

    print('No Suite with name ', feature_name, ' was found on TestRail')
    new_project_suite = Suite({
        'name': feature_name,
        'description': '',
        'is_baseline': False,
        'is_completed': False,
        'is_master': False,
        'project_id': tr_project_id
    })
    print('Creating new Suite ', feature_name)
    return tr.suites.add_suite(project_id=tr_project_id, suite=new_project_suite)


def get_suite_section(tr: TestRailAPI, project_id: int, tr_project_suite: Suite, suite_section) -> Section:
    print('Collecting Sections for suite ', tr_project_suite.name, ' from TestRail')
    tr_suite_sections = tr.sections.get_sections(project_id, tr_project_suite.id)
    if not any(tr_suite_section.name == suite_section['name'] for tr_suite_section in tr_suite_sections):
        suite_section['depth'] = 0
        suite_section['suite_id'] = tr_project_suite.id
        print('No Section with name %s was found for suite %s. Creating new Section.'
              % (suite_section['name'], tr_project_suite.name))
        tr_suite_sections.append(tr.sections.add_section(project_id=project_id, section=Section(suite_section)))
    return next(tr_suite_section for tr_suite_section in tr_suite_sections
                if tr_suite_section.name == suite_section['name'])
