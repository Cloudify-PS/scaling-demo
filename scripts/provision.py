from cloudify import ctx
from cloudify.state import ctx_parameters as p

networks = p['networks']
ctx.logger.info('networks from get_attribute: {}'.format(networks))
