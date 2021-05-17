# flake8: noqa E501
__copyright__ = "Copyright 2020-2021, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"


def setup_pydevd(host: str = "localhost", port: int = 5678) -> bool:
    """
    Setup pydevd debugging service

    Here is a sample (GlobeBuilder) Intellij Idea / PyCharm configuration for setting up the debug server in workspace.xml:

    <configuration name="Debug Server" type="PyRemoteDebugConfigurationType" factoryName="Python Remote Debug">
      <module name="QGIS Debug Server" />
      <option name="PORT" value="5678" />
      <option name="HOST" value="localhost" />
      <PathMappingSettings>
        <option name="pathMappings">
          <list>
            <mapping local-root="$PROJECT_DIR$/<plugin_name>" remote-root="/home/user/.local/share/QGIS/QGIS3/profiles/default/python/plugins/<plugin_name>" />
          </list>
        </option>
      </PathMappingSettings>
      <option name="REDIRECT_OUTPUT" value="true" />
      <option name="SUSPEND_AFTER_CONNECT" value="true" />
      <method v="2" />
    </configuration>

    :param host: host of the debug server
    :param port: port of the debug server
    :return: Whether debugger was initialized properly or not
    """
    succeeded = False
    try:
        import pydevd

        pydevd.settrace(host, port=port, stdoutToServer=True, stderrToServer=True)
        succeeded = True
    except Exception as e:
        print("Unable to create pydevd debugger: {}".format(e))

    return succeeded


def setup_ptvsd(host: str = "localhost", port: int = 5678) -> bool:
    """
    Setup ptvsd degugging service

    Currently, debugging with VSCode requires the deprecated ptvsd library, due to a bug in debugpy:
    https://github.com/microsoft/debugpy/issues/586

    Here is a sample VSCode configuration for connecting to the debug server in launch.json:

    {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/<plugin_name>",
                    "remoteRoot": "/Users/<user_name>/Library/Application Support/QGIS/QGIS3/profiles/edplanning/python/plugins/<plugin_name>"
                }
            ]
        }
    ]

    :param host: host of the debug server
    :param port: port of the debug server
    :return: Whether debugger was initialized properly or not
    """
    succeeded = False
    try:
        import ptvsd

        ptvsd.enable_attach((host, port))
        succeeded = True
    except Exception as e:
        print("Unable to create ptvsd debugger: {}".format(e))
    return succeeded


def setup_debugpy(host: str = "localhost", port: int = 5678) -> bool:
    """
    Setup debugpy degugging service

    :param host: host of the debug server
    :param port: port of the debug server
    :return: Whether debugger was initialized properly or not
    """
    succeeded = False
    try:
        import debugpy

        debugpy.listen((host, port))
        succeeded = True
    except Exception as e:
        print("Unable to create debugpy debugger: {}".format(e))
    return succeeded
