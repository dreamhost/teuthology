import argparse
import sys

import teuthology.openstack


def main(argv=sys.argv[1:]):
    teuthology.openstack.main(parse_args(argv), argv)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Run a suite of ceph integration tests. A suite is a directory containing
facets. A facet is a directory containing config snippets. Running a suite
means running teuthology for every configuration combination generated by
taking one config snippet from each facet. Any config files passed on the
command line will be used for every combination, and will override anything in
the suite. By specifying a subdirectory in the suite argument, it is possible
to limit the run to a specific facet. For instance -s upgrade/dumpling-x only
runs the dumpling-x facet of the upgrade suite.

Display the http and ssh access to follow the progress of the suite
and analyze results.

  firefox http://183.84.234.3:8081/
  ssh -i teuthology-admin.pem ubuntu@183.84.234.3

""")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true', default=None,
        help='be more verbose',
    )
    parser.add_argument(
        '--name',
        help='OpenStack primary instance name',
        default='teuthology',
    )
    parser.add_argument(
        '--key-name',
        help='OpenStack keypair name',
        required=True,
    )
    parser.add_argument(
        '--key-filename',
        help='path to the ssh private key',
    )
    parser.add_argument(
        '--simultaneous-jobs',
        help='maximum number of jobs running in parallel',
        type=int,
        default=1,
    )
    parser.add_argument(
        '--teardown',
        action='store_true', default=None,
        help='destroy the cluster, if it exists',
    )
    parser.add_argument(
        '--upload',
        action='store_true', default=False,
        help='upload archives to an rsync server',
    )
    parser.add_argument(
        '--archive-upload',
        help='rsync destination to upload archives',
        default='ubuntu@teuthology-logs.public.ceph.com:./',
    )
    # copy/pasted from scripts/suite.py
    parser.add_argument(
        'config_yaml',
        nargs='*',
        help='Optional extra job yaml to include',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true', default=None,
        help='Do a dry run; do not schedule anything',
    )
    parser.add_argument(
        '-s', '--suite',
        help='The suite to schedule',
    )
    parser.add_argument(
        '-c', '--ceph',
        help='The ceph branch to run against',
        default='master',
    )
    parser.add_argument(
        '-k', '--kernel',
        help=('The kernel branch to run against; if not '
              'supplied, the installed kernel is unchanged'),
    )
    parser.add_argument(
        '-f', '--flavor',
        help=("The kernel flavor to run against: ('basic',"
              "'gcov', 'notcmalloc')"),
        default='basic',
    )
    parser.add_argument(
        '-d', '--distro',
        help='Distribution to run against',
    )
    parser.add_argument(
        '--suite-branch',
        help='Use this suite branch instead of the ceph branch',
    )
    parser.add_argument(
        '-e', '--email',
        help='When tests finish or time out, send an email here',
    )
    parser.add_argument(
        '-N', '--num',
        help='Number of times to run/queue the job',
        type=int,
        default=1,
    )
    parser.add_argument(
        '-l', '--limit',
        metavar='JOBS',
        help='Queue at most this many jobs',
        type=int,
    )
    parser.add_argument(
        '--subset',
        help=('Instead of scheduling the entire suite, break the '
              'set of jobs into <outof> pieces (each of which will '
              'contain each facet at least once) and schedule '
              'piece <index>.  Scheduling 0/<outof>, 1/<outof>, '
              '2/<outof> ... <outof>-1/<outof> will schedule all '
              'jobs in the suite (many more than once).')
    )
    parser.add_argument(
        '-p', '--priority',
        help='Job priority (lower is sooner)',
        type=int,
        default=1000,
    )
    parser.add_argument(
        '--timeout',
        help=('How long, in seconds, to wait for jobs to finish '
              'before sending email. This does not kill jobs.'),
        type=int,
        default=43200,
    )
    parser.add_argument(
        '--filter',
        help=('Only run jobs whose description contains at least one '
              'of the keywords in the comma separated keyword '
              'string specified. ')
    )
    parser.add_argument(
        '--filter-out',
        help=('Do not run jobs whose description contains any of '
              'the keywords in the comma separated keyword '
              'string specified. ')
    )
    parser.add_argument(
        '--throttle',
        help=('When scheduling, wait SLEEP seconds between jobs. '
              'Useful to avoid bursts that may be too hard on '
              'the underlying infrastructure or exceed OpenStack API '
              'limits (server creation per minute for instance).'),
        type=int,
        default=15,
    )
    parser.add_argument(
        '--ceph-git-url',
        help=("git clone url for Ceph"),
    )
    parser.add_argument(
        '--ceph-qa-suite-git-url',
        help=("git clone url for ceph-qa-suite"),
    )

    return parser.parse_args(argv)
