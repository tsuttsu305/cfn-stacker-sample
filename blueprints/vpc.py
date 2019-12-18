from stacker.blueprints.base import Blueprint
from troposphere import Ref
from troposphere_mate import Output
import troposphere_mate.ec2 as ec2


class Vpc(Blueprint):
    VARIABLES = {
        "CidrBlock": {
            "type": str,
            "description": "Vpc CidrBlock"
        },
        "PublicSubnets": {
            "type": list,
            "description": "Public Subnet CidrBlock List"
        },
        "PrivateSubnets": {
            "type": list,
            "description": "Private Subnet CidrBlock List"
        }
    }

    def create_template(self):
        var = self.get_variables()

        self.template.description = "VPC Stack"

        vpc = self.template.add_resource(
            ec2.VPC(
                'Vpc',
                CidrBlock=var['CidrBlock'],
                EnableDnsHostnames=True,
                EnableDnsSupport=True
            )
        )
        self.template.add_output(Output('VpcId', Ref(vpc)))

        internet_gateway = self.template.add_resource(ec2.InternetGateway('Igw'))

        self.template.add_resource(
            ec2.VPCGatewayAttachment(
                'VpcGwAttachment',
                VpcId=Ref(vpc),
                InternetGatewayId=Ref(internet_gateway)
            )
        )

        default_route_table = self.template.add_resource(
            ec2.RouteTable(
                'DefaultRouteTable',
                VpcId=Ref(vpc)
            )
        )

        self.template.add_resource(
            ec2.Route(
                'DefaultRoute',
                RouteTableId=Ref(default_route_table),
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=Ref(internet_gateway)
            )
        )

        # Create Public Subnet
        for k, v in enumerate(var['PublicSubnets']):
            public_subnet = self.template.add_resource(
                ec2.Subnet(
                    f'PublicSubnet{k}',
                    CidrBlock=v,
                    VpcId=Ref(vpc)
                )
            )

            self.template.add_output(Output(f'PublicSubnet{k}', Ref(public_subnet)))

            self.template.add_resource(
                ec2.SubnetRouteTableAssociation(
                    f'PublicSubnetRouteTableAssociation{k}',
                    RouteTableId=Ref(default_route_table),
                    SubnetId=Ref(public_subnet)
                )
            )

        # Create Private Subnet
        for k, v in enumerate(var['PrivateSubnets']):
            private_subnet = self.template.add_resource(
                ec2.Subnet(
                    f'PrivateSubnet{k}',
                    CidrBlock=v,
                    VpcId=Ref(vpc)
                )
            )
            self.template.add_output(Output(f'PrivateSubnet{k}', Ref(private_subnet)))
