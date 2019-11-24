import argparse
from sys import stdout
from Peasant.banner import banner
import pdb

class Argument:

    def __init__(self,*args,**kwargs):

        self.args = args
        self.kwargs = kwargs

    def add(self,target):

        target.add_argument(*self.args,**self.kwargs)


# ===================
# OPERATIONAL OPTIONS
# ===================

company_names = Argument('-cns','--company-names',
    nargs='+',
    required=True,
    help='''Space delimited LinkedIn company names as observed in
    URL of company profile, e.g.: the identifier in the following URL
    would be 'black-hills-information-security:
    /company/black-hills-information-security/people/
    ''')
add_contacts = Argument('-ac','--add-contacts',
    action='store_true',
    help='''When possible, attempt to make a connection request
    for a contact. Default: %(default)s
    ''')

# ======================
# AUTHENTICATION OPTIONS
# ======================

credentials = Argument('-C','--credentials',
    help='''Colon delimited credentials, e.g. 'username:password', to
    use for authentication.
    ''')
cookies = Argument('-c','--cookies',
    help='''Cookies needed to access LinkedIn in context of the correct
    user. During development, the following cookies were required: li_at
    and JSESSIONID'
    ''')

# ==============
# OUTPUT OPTIONS
# ==============

output_file = Argument('-of','--output-file',
    default=stdout,
    help='''Name of file to receive CSV output (Default: stdout). If a
    file name is provided and that file already exists, it will be read
    into memory and be treated as previous output. This provides a level
    of efficiency by allowing the scrept to avoid sending multiple connection
    requests for the same profile.
    ''')

# ============
# MISC OPTIONS
# ============

url = Argument('-u','--url',
    default='https://www.linkedin.com',
    help='Base URL to target for requests. Default: %(default)s')
proxies = Argument('-p','--proxies',
    nargs='+',
    default=[],
    help='''Space delimited series of upstream proxies that will
    be used to send requests.''',
    required=False)
user_agent = Argument('-ua','--user-agent',
    default='Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101' \
        'Firefox/60.0',
    help='User agent string. Default: %(default)s')
verify_ssl = Argument('-vs','--verify-ssl',
    action='store_true',
    help='Verify SSL certificate. Default: %(default)s')

# =============
# OTHER OPTIONS
# =============

public_identifier = Argument('-pu','--public-identifier',
        help='Public identifier of target profile',
        required=True)
input_file = Argument('-if','--input-file',
        help='Input CSV file to extract records',
        required=True)

# == END ARGUMENT DEFINITION ==

parser = argparse.ArgumentParser(
    description=f'''Detect, generate, and collect connection requests
    from LinkedIn'''
)

subparsers = parser.add_subparsers(help='subcommand help')

# =================
# HARVEST SUBPARSER
# =================
harvest = subparsers.add_parser('harvest')

# Operational options
operational_group = harvest.add_argument_group('Operational Parameters (REQUIRED)',
        description='''Determine the companies to target and
        if connection requests should be generated.''')
company_names.add(operational_group)
add_contacts.add(operational_group)

# Auth Options
auth_options = harvest.add_argument_group('Authentication Parameters (OPTIONAL)',
        description='''Determine how to authenticate to LinkedIn. User is
        prompted for credentials if one of these mutually-exclusive options
        are not provided.
        ''')
credential_group = auth_options.add_mutually_exclusive_group()
credentials.add(credential_group)
cookies.add(credential_group)

# Output Options
output_group = harvest.add_argument_group('Output Parameters (OPTIONAL)',
        description='Configure output options.')
output_file.add(output_group)

# MISC Options
misc_group = harvest.add_argument_group('Miscellaneous Parameters (OPTIONAL)',
        description='Additional parameters with sane defaults')
url.add(misc_group)
proxies.add(misc_group)
user_agent.add(misc_group)
verify_ssl.add(misc_group)

# ======================
# ADD CONTACTS SUBPARSER
# ======================

add_contacts = subparsers.add_parser('add_contacts')
input_options = add_contacts.add_argument_group(
        'Input Options (REQUIRED)'
    )
input_file.add(input_options)

# Auth Options
auth_options = add_contacts.add_argument_group('Authentication Parameters (OPTIONAL)',
        description='''Determine how to authenticate to LinkedIn. User is
        prompted for credentials if one of these mutually-exclusive options
        are not provided.
        ''')
credential_group = auth_options.add_mutually_exclusive_group()
credentials.add(credential_group)
cookies.add(credential_group)

# MISC Options
misc_group = add_contacts.add_argument_group('Miscellaneous Parameters (OPTIONAL)',
        description='Additional parameters with sane defaults')
url.add(misc_group)
proxies.add(misc_group)
user_agent.add(misc_group)
verify_ssl.add(misc_group)

# ===============
# SPOOF SUBPARSER
# ===============

spoof = subparsers.add_parser('spoof_profile')

# Targeting Options
targeting_options = spoof.add_argument_group(
        'Targeting Options (REQUIRED)')
public_identifier.add(targeting_options)

# Auth Options
auth_options = spoof.add_argument_group('Authentication Parameters (OPTIONAL)',
        description='''Determine how to authenticate to LinkedIn. User is
        prompted for credentials if one of these mutually-exclusive options
        are not provided.
        ''')
credential_group = auth_options.add_mutually_exclusive_group()
credentials.add(credential_group)
cookies.add(credential_group)

# MISC Options
misc_group = spoof.add_argument_group('Miscellaneous Parameters (OPTIONAL)',
        description='Additional parameters with sane defaults')
url.add(misc_group)
proxies.add(misc_group)
user_agent.add(misc_group)
verify_ssl.add(misc_group)
