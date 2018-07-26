from __future__ import print_function

import json
from testrail.case import Case
from testrail.client import TestRail
from testrail.entry import Entry
from testrail.helper import TestRailError
from testrail.result import Result
from testrail.section import Section
from testrail.suite import Suite


def initialize_testrail_client(project_id):
    # Instantiate the TestRail client
    # Use the CLI argument to identify which project to work with
    print('Initialize TestRail client')
    return TestRail(project_id)


def publish_tests(tr, project_name, feature):
    # Get a reference to the current project and dependencies
    print('Collecting Project %s from TestRail' % project_name)
    # pylint: disable=protected-access
    tr_project = tr.project(tr._project_id)

    feature_name = feature['feature']['name'].strip()
    feature_description = feature['feature']['description'].replace('\n  ', '\n').strip()
    tr_project_suite = get_project_suite(tr, tr_project, feature_name, feature_description)

    tr_suite_section = get_suite_section(tr, tr_project_suite)

    print('Collecting Cases for suite %s from TestRail' % tr_project_suite.name)
    tr_suite_cases = tr.cases(tr_project_suite)

    raw_custom_preconds = []
    for scenario in feature['feature']['children']:
        if scenario['keyword'] == 'Background':
            print('Collecting Case preconditions')
            raw_custom_preconds = list('**' + rs['keyword'] + ':** ' + rs['text'] for rs in scenario['steps'])
            continue

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
                build_case(tr, tr_project_suite, tr_suite_cases, tr_suite_section, feature, scenario,
                           raw_custom_preconds, raw_custom_data_set)
        else:
            build_case(tr, tr_project_suite, tr_suite_cases, tr_suite_section, feature, scenario,
                       raw_custom_preconds, None)


# pylint: disable=too-many-arguments
def build_case(tr, tr_project_suite, tr_suite_cases, tr_suite_section, feature, scenario, raw_custom_preconds,
               raw_custom_data_set):
    # Setting Case references
    feature_refs = filter(lambda sc: '-' in sc['name'], feature['feature']['tags'])
    scenario_refs = filter(lambda sc: '-' in sc['name'], scenario['tags'])
    raw_refs = ', '.join(tg['name'].replace('@','') for tg in (feature_refs + scenario_refs))

    # Setting Case priority
    priority_name = 'Critical' if filter(lambda sc: 'smoke' in sc['name'], scenario['tags']) \
        else 'High' if filter(lambda sc: 'sanity' in sc['name'], scenario['tags']) \
        else 'Medium' if filter(lambda sc: 'regression' in sc['name'], scenario['tags']) \
        else 'Low'
    raw_priority = next((pr.id for pr in tr.priorities() if pr.name == priority_name), None)

    # Setting Case type
    raw_type = next((ct.id for ct in tr.case_types() if ct.name == 'Functional'), None)

    # Setting Case template
    raw_template = next((ct.id for ct in tr.templates() if ct.name == 'Test Case (Steps)'), None)

    # Setting Case automation
    raw_custom_automation_type = '1' if any('automated' in sc['name'] for sc in scenario['tags']) else '0'

    # Setting Case steps
    raw_steps = list({'content': rs, 'expected': ''} for rs in raw_custom_preconds)
    raw_steps.extend(list({'content': '**' + rs['keyword'].strip() + ':** ' + rs['text'].strip(), 'expected': ''}
                          for rs in scenario['steps']))
    raw_case = Case({
        'estimate': '10m',
        'priority_id': raw_priority,
        'refs': raw_refs,
        'suite_id': tr_project_suite.id,
        'section_id': tr_suite_section.id,
        'title': scenario['name'],
        'type_id': raw_type,
        'template_id': raw_template,
        'custom_automation_type': raw_custom_automation_type,
        'custom_data_set': raw_custom_data_set,
        'custom_preconds': '\n'.join(str(rp) for rp in raw_custom_preconds),
        'custom_steps_separated': raw_steps
    })
    export_case(tr, tr_suite_cases, raw_case)


def export_case(tr, tr_suite_cases, raw_case):
    # pylint: disable=protected-access
    tr_suite_case = next((sc for sc in tr_suite_cases
                          if sc.title == raw_case.title
                          and sc._custom_methods['custom_data_set'] == raw_case._custom_methods['custom_data_set'])
                         , None)
    if tr_suite_case:
        print('Upgrading Case ', tr_suite_case.title)
        raw_case.id = tr_suite_case.id
        tr.update_case(raw_case)
    else:
        print('Creating Case ', raw_case.title)
        tr.add_case(raw_case)


def get_test_from_scenario(tr, tr_test_plan, test_env, request, feature, scenario):
    data_set_dict = {k: str(v) for k, v in request.node.funcargs.items() if k not in 'request'}
    data_set = json.dumps(data_set_dict, indent=4, ensure_ascii=False)

    tr_plan_entry = next((pe for pe in tr_test_plan.entries if pe.name == '%s - %s' % (feature.name, test_env)),
                         None)
    if not tr_plan_entry:
        return 'Feature %s not imported to TestRail' % feature.name
    tr_run_tests = tr.tests(tr_plan_entry.runs[0])

    tr_run_test = next((rt for rt in tr_run_tests
                        if rt.title == scenario.name
                        and (rt.custom_methods['custom_data_set'] == data_set
                             or data_set_dict == {})),
                       None)
    if not tr_run_test:
        return 'Scenario %s not imported to TestRail' % scenario.name

    tr_statuses = tr.statuses()
    custom_step_results = []
    custom_steps_separated = tr_run_test.custom_methods['custom_steps_separated']
    for scenario_step, tr_case_step in zip(scenario.steps, custom_steps_separated):
        status_type = 'passed' if not scenario_step.failed \
            else 'failed' if scenario_step.failed \
            else 'untested'
        exception_message = '' if scenario_step.failed is False or scenario_step.failed is None \
            else scenario.exception.msg if hasattr(scenario.exception, 'msg') \
            else scenario.exception.message if hasattr(scenario.exception, 'message') \
            else ''
        custom_step_results.append({
            'content': tr_case_step['content'],
            'expected': tr_case_step['expected'],
            'actual': exception_message,
            'status_id': next(st.id for st in tr_statuses if st.name == status_type)
        })
    status_type = 'passed' if not scenario.failed else 'failed' if scenario.failed else 'untested'
    tr_result = Result({
        'test_id': tr_run_test.id,
        'status_id': next(st.id for st in tr_statuses if st.name == status_type),
        'comment': '',
        'custom_step_results': custom_step_results
    })

    return {'test': tr_run_test, 'result': tr_result}


def publish_tests_results(tr, tr_test_plan, test_run, test_env):
    print('\nPublishing results')
    for key in test_run:
        tr_results = []
        for test_run_item in test_run[key]:
            tr_plan_entry = next(pe for pe in tr_test_plan.entries if pe.name == '%s - %s' % (key, test_env))
            tr_results.append(test_run_item['result'])

        tr.add_results((tr_plan_entry.runs[0], tr_results))
    print('\nResults published')


def setup_test_plan(tr, project_name, test_plan, test_env, test_market, test_scope):
    tr_plan_name = project_name + '_' + test_plan
    tr_run_name = '%s - ' + test_env

    tr_plan = get_project_test_plan(tr, tr_plan_name, test_market)

    # Check and add if needed Suites to Test Plan for the given Test Env
    for suite in tr.suites():
        is_filter = True if test_scope.__len__() == 0 \
            else True if test_scope.__len__() != 0 and suite.name in test_scope.values() \
            else False
        if is_filter \
                and not any(tr_plan_run.name == tr_run_name % suite.name for tr_plan_run in tr_plan.entries):
            print('!Entry %s is not part of the Test Plan %s... Creating it.'
                  % (tr_run_name % suite.name, tr_plan_name))
            raw_plan_entry = Entry({
                'suite_id': suite.id,
                'name': tr_run_name % suite.name,
                'description': '',
                'include_all': True
            })
            tr.add_plan_entry(raw_plan_entry, tr_plan.id)

    return get_project_test_plan(tr, tr_plan_name, test_market)


def get_project_test_plan(tr, tr_plan_name, test_market):
    test_plan_name = '%s_%s' % (tr_plan_name, test_market)
    tr_plans = tr.plans()
    tr_plan = next((tp for tp in tr_plans if tp.name == test_plan_name), None)
    if tr_plan is None:
        error_message = 'There is no Test Plan with name %s set on TestRail' % test_plan_name
        raise TestRailError(error_message)
    print('Collecting Test Plan ', tr_plan.name, ' from TestRail')
    return tr_plan


def get_project_suite(tr, tr_project, feature_name, feature_description):
    tr_project_suites = tr.suites()
    if any((tr_project_suite.name == feature_name and tr_project_suite.description == feature_description)
           for tr_project_suite in tr_project_suites):
        print('Collecting Suite ', feature_name, ' from TestRail')
        return next((ps for ps in tr_project_suites
                     if (ps.name == feature_name and ps.description == feature_description)))

    print('No Suite with name ', feature_name, ' was found on TestRail')
    raw_project_suite = Suite({
        'name': feature_name,
        'description': feature_description,
        'is_baseline': False,
        'is_completed': False,
        'is_master': False,
        'project_id': tr_project.id
    })
    print('Creating new Suite ', feature_name)
    return tr.add_suite(raw_project_suite)


def get_suite_section(tr, tr_project_suite):
    print('Collecting Sections for suite ', tr_project_suite.name, ' from TestRail')
    tr_suite_sections = tr.sections(tr_project_suite)
    if not tr_suite_sections:
        print('No Section was found for suite ', tr_project_suite.name, ' on TestRail')
        raw_suite_section = Section({
            'name': 'Test Cases',
            'description': 'Default Suite section',
            'depth': 0,
            'display_order': 1,
            'suite_id': tr_project_suite.id
        })
        print('Creating new Section ', raw_suite_section.name)
        tr_suite_sections.append(tr.add_section(raw_suite_section))
    return tr_suite_sections[0]
