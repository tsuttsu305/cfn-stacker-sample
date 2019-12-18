from stacker.blueprints.base import Blueprint
import troposphere_mate.ec2 as ec2


class Instance(Blueprint):
    VARIABLES = {
        "SubnetId": {
            "type": str,
            "description": "Target Subnet ID"
        },
        "ImageId": {
            "type": str,
            "description": "Image ID"
        }
    }

    def create_template(self):
        var = self.get_variables()

        self.template.description = "Instance Stack"

        self.template.add_resource(
            ec2.Instance(
                'Instance',
                ImageId=var['ImageId'],
                SubnetId=var['SubnetId'],
                InstanceType='t3.micro'
            )
        )

