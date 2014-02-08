from fabric.context_managers import cd
from fabric.contrib.files import append, sed
from fabric.operations import sudo
from fabric.state import env

__author__ = 'calthorpe_associates'

HADOOP_VERSION = '1.0.3'

from installation import JAVA_RESPOSITORY, JAVA_VERSION

def install_hadoop():
    sudo('addgroup hadoop')
    sudo('adduser --ingroup hadoop hduser')
    sudo('ssh-keygen -t rsa -P "" -f /home/hduser/.ssh/id_rsa', user='hduser')
    sudo('cat /home/hduser/.ssh/id_rsa.pub >> /home/hduser/.ssh/authorized_keys', user='hduser')
    sudo('ssh-keyscan -H {0} >> /home/hduser/.ssh/known_hosts'.format(env.host), user='hduser')
    sudo('wget -O /usr/local/hadoop-{0}.tar.gz '
         'http://mirrors.ibiblio.org/apache/hadoop/core/hadoop-{0}/hadoop-{0}.tar.gz'.format(HADOOP_VERSION))
    with cd('/usr/local'):
        sudo('tar xzf hadoop-{0}.tar.gz'.format(HADOOP_VERSION))
        sudo('chown -R hduser:hadoop hadoop-{0}'.format(HADOOP_VERSION))
        sudo('ln -s hadoop-{0} hadoop'.format(HADOOP_VERSION))
        # Edit .bashrc
    # APPEND JAVA_HOME if it doesn't exist yet
    append('/home/hduser/.bashrc', 'export JAVA_HOME=/usr/lib/jvm/{0}'.format(JAVA_VERSION), use_sudo=True)
    append('/home/hduser/.bashrc', '''# Set Hadoop-related environment variables
export HADOOP_HOME=/usr/local/hadoop

# Some convenient aliases and functions for running Hadoop-related commands
unalias fs &> /dev/null
alias fs="hadoop fs"
unalias hls &> /dev/null
alias hls="fs -ls"

# If you have LZO compression enabled in your Hadoop cluster and
# compress job outputs with LZOP (not covered in this tutorial):
# Conveniently inspect an LZOP compressed file from the command
# line; run via:
#
# $ lzohead /hdfs/path/to/lzop/compressed/file.lzo
#
# Requires installed lzop command.
#
lzohead () {
    hadoop fs -cat $1 | lzop -dc | head -1000 | less
}

# Add Hadoop bin/ directory to PATH
export PATH=$PATH:$HADOOP_HOME/bin''', use_sudo=True)
    sed('/usr/local/hadoop/conf/hadoop-env.sh', r'^# export JAVA_HOME=.*',
        '# export JAVA_HOME=/usr/lib/jvm/{0}'.format(JAVA_VERSION), backup='', use_sudo=True)
    sudo('mkdir -p /app/hadoop/tmp')
    sudo('sudo chown hduser:hadoop /app/hadoop/tmp')
    sudo('/usr/local/hadoop/bin/hadoop namenode -format', user='hduser')
    # Remove the </configuration> and append a configuration block
    sed('/usr/local/hadoop/conf/core-site.xml', r'^</configuration>', '', backup='', use_sudo=True)
    append('/usr/local/hadoop/conf/core-site.xml', '''
    <property>
      <name>hadoop.tmp.dir</name>
      <value>/app/hadoop/tmp</value>
      <description>A base for other temporary directories.</description>
    </property>

    <property>
      <name>fs.default.name</name>
      <value>hdfs://localhost:54310</value>
      <description>The name of the default file system.  A URI whose
      scheme and authority determine the FileSystem implementation.  The uris scheme determines the config property \(fs.SCHEME.impl\) naming
      the FileSystem implementation class.  The uris authority is used to
      determine the host, port, etc. for a filesystem.</description>
    </property>
</configuration>''', use_sudo=True, escape=True)

    sed('/usr/local/hadoop/conf/mapred-site.xml', r'^</configuration>', '', backup='', use_sudo=True)
    append('/usr/local/hadoop/conf/mapred-site.xml', '''
    <!-- In: conf/mapred-site.xml -->
    <property>
      <name>mapred.job.tracker</name>
      <value>localhost:54311</value>
      <description>The host and port that the MapReduce job tracker runs
      at.  If "local", then jobs are run in-process as a single map
      and reduce task.
      </description>
    </property>
</configuration>''', use_sudo=True)

    sed('/usr/local/hadoop/conf/hdfs-site.xml', r'^</configuration>', '', backup='', use_sudo=True)
    append('/usr/local/hadoop/conf/hdfs-site.xml', '''
    <!-- In: conf/hdfs-site.xml -->
    <property>
      <name>dfs.replication</name>
      <value>1</value>
      <description>Default block replication.
      The actual number of replications can be specified when the file is created.
      The default is used if replication is not specified in create time.
      </description>
    </property>
</configuration>''', use_sudo=True)
    start_hadoop()


def configure_hadoop_cluster():
    all_hosts = env.all_hosts
    for slave in env.roledefs['slave']:
        sudo('ssh-copy-id -i /home/hduser/.ssh/id_rsa.pub hduser@{0}'.format(slave), user='hduser')
    if (env.host in env.roledefs['master']):
        configure_as_hadoop_master()
    else:
        configure_as_hadoop_slave()


def configure_as_hadoop_master():
    pass


def configure_as_hadoop_slave():
    master = env.roledefs['master'][0]
    # Run this so that the slave automatically accepts the master on the first ssh, to avoid the prompt
    sudo('ssh-keyscan -H {0} >> /home/hduser/.ssh/known_hosts'.format(master), user='hduser')


def start_hadoop():
    sudo('/usr/local/hadoop/bin/start-all.sh')


def stop_hadoop():
    sudo('/usr/local/hadoop/bin/stop-all.sh', user='hduser')

