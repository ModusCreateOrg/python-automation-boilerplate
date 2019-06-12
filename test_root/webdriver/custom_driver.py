

# pylint: disable=protected-access
def driver_kwargs(request, capabilities, **kwargs):
    executor = 'http://{0.appium_host}:{0.appium_port}/wd/hub'.format(request.__config.option)
    variables = request.__config._variables['appium']
    kwargs = dict(
        command_executor=executor,
        desired_capabilities=appium_capabilities(capabilities, variables),
        browser_profile=None,
        proxy=None,
        keep_alive=False,
    )
    return kwargs


def appium_capabilities(capabilities, variables):
    capabilities.update(variables)
    return capabilities
