from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck


class ALBDropHttpHeaders(BaseResourceCheck):

    def __init__(self):
        name = "Ensure that ALB drops HTTP headers"
        id = "CKV_AWS_131"
        supported_resources = ["AWS::ElasticLoadBalancingV2::LoadBalancer"]
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        # alb is default loadbalancer type if not explicitly set
        alb = True

        properties = conf.get("Properties")
        lb_type = properties.get("Type")
        if lb_type != None and lb_type != 'application':
            print(lb_type)
            alb = False

        # If lb is alb then drop headers must be present and true 
        if alb:
            lb_attributes = properties.get('LoadBalancerAttributes', {})
            if isinstance(lb_attributes, list):
                for item in lb_attributes:
                    key = item.get('Key')
                    value = item.get('Value')
                    #print(key)
                    #print(value)
                    if key == 'routing.http.drop_invalid_header_fields.enabled' and value == "true":
                        return CheckResult.PASSED
            return CheckResult.FAILED

        # if lb is not alb then check is not valid
        print("well there ya go")
        return CheckResult.UNKNOWN


check = ALBDropHttpHeaders()
