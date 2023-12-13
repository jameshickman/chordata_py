from src.chordata.server_env import ServerEnvironment


def tenant_prefix(e: ServerEnvironment) -> str:
    if e.get_configuration().get('tenant_database') is not None:
        return '/_' + e.get_tenant()
    return ''
