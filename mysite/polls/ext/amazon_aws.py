from . import CloudProvider, log
import boto, boto.ec2, boto.iam, boto.vpc, time
import json
from jinja2 import Template

# wait 5 seconds before retrying after failed requests
WAITING_TIME = 5
CREDENTIALS_FILE_NAME = "aws_credentials.json"
TEMPLATE_FILE_NAME = "aws_subnet_policy.jinja"

class AWSProvider(CloudProvider):

###############################################################################
    _config_path = None
    _credentials = None
    _ec2_conn = None
    _vpc_conn = None
    _iam_conn = None
    """
    # credentials should not be loaded like this
    def __init__(self, config_path):
        self._config_path = config_path
        # check credentials
        sel_get_credentials()

    def _get_credentlsials(self):
        if not self._credentials:
            credential_file = self._config_path + CREDENTIALS_FILE_NAME
            try:
                with open(credential_file) as json_credentials:
                    self._credentials = json.load(json_credentials)
            except IOError:
                log(
                    "Error",
                    "Could not read '" + credential_file + "'! Quitting"
                )
                exit(1)
        return self._credentials
    """

    def _get_ec2_connection(self, region_name):
        if not self._ec2_conn:
            #credentials = self._get_credentials()
            self._ec2_conn = boto.ec2.connect_to_region(
                region_name=region_name,
                #aws_access_key_id=credentials['id'],
                #aws_secret_access_key=credentials['key']
            )
        return self._ec2_conn


    def _get_vpc_connection(self, region_name):
        if not self._vpc_conn:
            #credentials = self._get_credentials()
            self._vpc_conn = boto.vpc.connect_to_region(
                region_name=region_name,
                #aws_access_key_id=credentials['id'],
                #aws_secret_access_key=credentials['key']
            )
        return self._vpc_conn


    def _get_iam_connection(self):
        if not self._iam_conn:
            #credentials = self._get_credentials()
            self._iam_conn = boto.connect_iam(
                #aws_access_key_id=credentials['id'],
                #aws_secret_access_key=credentials['key']
            )
        return self._iam_conn


    def _tag_with_name(self, item, name):
        """ This function will tag a resource with a name """
        item.add_tag('Name', name)


    def _generate_subnet_policy(self, region_name, subnet_id):
        account_id = self._get_credentials()["account_id"]
        with open(self._config_path + TEMPLATE_FILE_NAME, "r") as tfile:
            template = Template(tfile.read())
            return template.render(
                account_id=account_id,
                region_name=region_name,
                subnet_id=subnet_id
            )


    ###########################################################################

    def create_permissions(self, instance_name, policy):
        """ Attaches a given policy to an instance """

        iam_conn = self._get_iam_connection()

        role_name = "cloudctl.role." + instance_name + str(int(time.time()))
        profile_name = "cloudctl.profile." + instance_name + str(int(time.time()))

        role = iam_conn.create_role(role_name)
        instance_profile = iam_conn.create_instance_profile(profile_name)
        iam_conn.add_role_to_instance_profile(profile_name, role_name)
        iam_conn.put_role_policy(role_name, profile_name, policy)
        return role_name, profile_name


    def create_instance(self, region, subnet_id, name, is_privileged=False):
        """ Creates an instance """
        instance_profile = None
        key_pair_name = ""
        if is_privileged:
            log(
                region,
                "creating privileged instance '" + name + "'"
            )
            role, instance_profile = self.create_permissions(
                name,
                self._generate_subnet_policy(region, subnet_id)
            )
            key_pair_name = instance_profile
            # sleep to make sure it's available when we need it
            time.sleep(10)
        else:
            key_pair_name = "cloudctl.profile." + name + str(int(time.time()))
            log(
                region,
                "creating instance '" + name + "'"
            )

        ec2_conn = self._get_ec2_connection(region)

        created = False
        while not created:
            try:
                key_pair = ec2_conn.create_key_pair(key_pair_name)
                created = True
            except boto.exception.EC2ResponseError:
                time.sleep(5)

        created = False
        while not created:
            try:
                reservation = ec2_conn.run_instances(
                    'ami-89634988',
                    instance_type='t2.micro',
                    subnet_id=subnet_id,
                    key_name=instance_profile,
                    instance_profile_name=instance_profile
                )
                created = True
            except:
                time.sleep(5)

        self._tag_with_name(reservation.instances[0], name)

        return reservation.instances[0].id, key_pair


    def create_vpc(self, vpc_name, vpc_region, cidr_block):
        """ Creates a VPC """
        log(
            vpc_region,
            "creating VPC '" + vpc_name + "'"
        )

        conn = self._get_vpc_connection(vpc_region)
        vpc = conn.create_vpc(cidr_block)
        self._tag_with_name(vpc, vpc_name)
        return vpc.id


    def shutdown_all_instances_in_subnet(self, region_name, subnet_id):
        conn = self._get_ec2_connection(region_name)

        instance_ids = []
        instance_profiles = []

        # find all instances in subnet
        for reservation in conn.get_all_reservations(
            filters=[("subnet-id", subnet_id)]
        ):
            for instance in reservation.instances:
                # set instance block devices to 'terminate on shutdown'
                instance.modify_attribute(
                    'blockDeviceMapping',
                    {'/dev/sda1': True}
                )

                # collect instance_ids
                instance_ids.append(instance.id)
                # collect instance_profiles
                instance_profiles.append(
                    instance.instance_profile["arn"].split("/")[1]
                )

        # TODO: delete all collected instance_profiles
        """
        if instance_profiles:
            for name in instance_profiles:
                conn.iam.delete_instance_profile(name)
                # TODO: delete policy
                # TODO: delete role
        """

        # terminate all collected instance_ids
        shutdown = False
        if instance_ids:
            log(
                region_name,
                "shutting down " + str(len(instance_ids)) + " instances..."
            )
            while not shutdown:
                try:
                    conn.terminate_instances(instance_ids=instance_ids)
                    shutdown = True
                except boto.exception.EC2ResponseError:
                    time.sleep(WAITING_TIME)


    def delete_subnet(self, region_name, subnet_id):
        vpc_conn = self._get_vpc_connection(region_name)
        log(
            region_name,
            "shutting down subnet '" + subnet_id + "'"
        )

        deleted = False
        while not deleted:
            try:
                vpc_conn.delete_subnet(subnet_id)
                deleted = True

            except boto.exception.EC2ResponseError as e:
                if (e.code == "DependencyViolation"):
                    time.sleep(5)



    def delete_vpc(self, region_name, vpc_id):
        """ Completely deletes a VPC with all its subnets and instances """
        vpc_conn = self._get_vpc_connection(region_name)

        # delete all subnets
        for subnet in vpc_conn.get_all_subnets(filters=[('vpcId', vpc_id)]):
            self.shutdown_all_instances_in_subnet(region_name, subnet.id)
            self.delete_subnet(region_name, subnet.id)

        # delete vpc
        deleted = False
        log(
            region_name,
            "shutting down VPC '" + vpc_id + "'"
        )

        while not deleted:
            try:
                result = vpc_conn.delete_vpc(vpc_id)
                deleted = True
                return result
            except boto.exception.EC2ResponseError as e:
                if (e.code == "DependencyViolation"):
                    time.sleep(5)



    def create_subnet(self, region_name, vpc_id, subnet_name, cidr_block, availability_zone):
        log(
            availability_zone,
            "Creating Subnet '" + subnet_name + "'"
        )

        conn = self._get_vpc_connection(region_name)
        subnet = conn.create_subnet(vpc_id, cidr_block, availability_zone)
        self._tag_with_name(subnet, subnet_name)
        return subnet.id


    def get_vpc_status(self, region_name, vpc_id):
        vpc_conn = self._get_vpc_connection(region_name)
        try:
            for vpc in vpc_conn.vpc.get_all_vpcs(vpc_ids=vpc_id):
                return vpc.state == "available"
        except boto.exception.EC2ResponseError as e:
            if e.code == "InvalidVpcID.NotFound":
                return False

    ###########################################################################

    def has_public_ip(self, region, instance_id):
        """ UNTESTED PRELIMINARY IMPLEMENTATION """
        ec2_conn = self._get_ec2_connection(region)

        for address in ec2_conn.get_all_addresses(filters=[("instance-id", instance_id)]):
            if address.public_ip:
                return True
        return False


    """ This function enables us to view the permissions that we have just created


    def view_permissions(vpc):
        conn = connect("")
        roles = 1 # conn.iam.list_roles()
        instance_profile = conn.iam.list_instance_profiles()
        ins_roles = 1 #conn.iam.list_instance_profiles_for_role('role')
        return {'roles':roles,'ins_roles':ins_roles,'instance_profile':instance_profile}
    """
